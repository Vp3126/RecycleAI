import streamlit as st
import numpy as np
import cv2
import pandas as pd
from PIL import Image
import io
import time
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Get the directory where app.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Waste Classification System",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Load CSS from file
def load_css():
    try:
        # Get the absolute path to the CSS file
        css_path = os.path.join(SCRIPT_DIR, "style.css")
        print(f"Attempting to load CSS from: {css_path}")  # Debug print
        
        if not os.path.exists(css_path):
            print(f"CSS file not found at: {css_path}")  # Debug print
            return
            
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
            print("CSS loaded successfully!")  # Debug print
    except Exception as e:
        print(f"Error loading CSS: {str(e)}")  # Debug print
        st.warning(f"Could not load custom CSS: {str(e)}")

# Load CSS
load_css()

# Add error handling for imports
try:
    from model import load_model, preprocess_image, predict_waste_class
    from utils import save_classification_history, get_classification_history
    from waste_info import waste_categories, get_recycling_instructions
except Exception as e:
    st.error(f"Error importing modules: {str(e)}")
    st.stop()

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state.history = []
if 'model' not in st.session_state:
    st.session_state.model = None
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

# Get query parameters
query_params = st.query_params
if 'category' in query_params:
    st.session_state.selected_category = query_params['category']

# Sidebar with error handling
with st.sidebar:
    try:
        logo_path = os.path.join(SCRIPT_DIR, "assets", "recycle_logo.svg")
        st.image(logo_path, width=100)
    except:
        st.markdown("♻️")

    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h1 style='color: #4CAF50; font-size: 1.5rem; margin-bottom: 10px;'>Waste Classification</h1>
            <p style='font-size: 0.9rem;'>Upload an image of waste to classify it and get recycling guidance.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='margin: 20px 0; border-color: #4CAF50;'>", unsafe_allow_html=True)

    # Navigation links
    st.markdown("<h3 style='color: #4CAF50; margin-bottom: 15px;'>Navigation</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div style='display: flex; flex-direction: column; gap: 10px;'>
            <a href='/' style='text-decoration: none; color: #4CAF50; padding: 10px; border-radius: 5px; background-color: #f1f8e9;'>🏠 Home</a>
            <a href='/dashboard' style='text-decoration: none; color: #4CAF50; padding: 10px; border-radius: 5px; background-color: #f1f8e9;'>📊 Dashboard</a>
            <a href='/education' style='text-decoration: none; color: #4CAF50; padding: 10px; border-radius: 5px; background-color: #f1f8e9;'>📚 Education</a>
            <a href='/about' style='text-decoration: none; color: #4CAF50; padding: 10px; border-radius: 5px; background-color: #f1f8e9;'>ℹ️ About</a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 20px 0; border-color: #4CAF50;'>", unsafe_allow_html=True)

    # Categories in sidebar
    st.markdown("<h3 style='color: #4CAF50; margin-bottom: 15px;'>Categories</h3>", unsafe_allow_html=True)
    for category in waste_categories.keys():
        if st.button(f"📦 {category.title()}", key=f"cat_{category}", use_container_width=True):
            st.session_state.selected_category = category
            st.rerun()

    # Sidebar
    st.sidebar.markdown("""
        <div>
            <h2 style='color: #4CAF50;'>🔄 Recent Classifications</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.history) > 0:
        for entry in reversed(st.session_state.history[-5:]):  # Show last 5 entries
            st.sidebar.markdown(f"""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #4CAF50;'>
                    <p style='margin: 0;'><strong>Category:</strong> {entry["category"].title()}</p>
                    <p style='margin: 5px 0 0 0; font-size: 0.9em;'>{entry["timestamp"]}</p>
                    <div style='margin-top: 10px;'>
                        <div style='background-color: #4CAF50; height: 4px; width: {entry["confidence"]}%; border-radius: 2px;'></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px;'>
                No classifications yet. Upload an image to get started!
            </div>
        """, unsafe_allow_html=True)

# App title
st.title("♻️ Waste Classification System")

# Load model with error handling
@st.cache_resource
def get_model():
    try:
        # Get the absolute path to the model file
        model_path = os.path.join(SCRIPT_DIR, "waste_model.pth")
        if not os.path.exists(model_path):
            st.error(f"Model file not found at: {model_path}")
            return None
            
        print(f"Attempting to load model from: {model_path}")
        model = load_model()
        
        if model is None:
            st.error("Failed to load model. Please check if waste_model.pth exists and is valid.")
            return None
            
        print("Model loaded successfully!")
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        print(f"Detailed error: {str(e)}")  # For debugging
        return None

# Try to load the model
try:
    if st.session_state.model is None:
        with st.spinner("Loading AI model..."):
            st.session_state.model = get_model()
        if st.session_state.model is not None:
            st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    print(f"Detailed error: {str(e)}")  # For debugging

# Main content
if st.session_state.selected_category and st.session_state.selected_category in waste_categories:
    selected_category = st.session_state.selected_category
    category_data = waste_categories[selected_category]
    
    st.header(f"{selected_category.title()} Waste")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("About")
        st.write(category_data["description"])
        
        st.subheader("Key Characteristics")
        for char in category_data["characteristics"]:
            st.markdown(f"✓ {char}")
    
    with col2:
        st.subheader("Recycling Instructions")
        st.markdown(category_data["recycling_instructions"])
        
        st.markdown("---")
        if st.button("🔙 Back to Home", use_container_width=True):
            st.session_state.selected_category = None
            st.rerun()

else:
    # Regular upload interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
            <div style='background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h2 style='color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;'>Upload Waste Image</h2>
                <p style='background-color: #f8f9fa; padding: 10px; border-radius: 5px; border-left: 4px solid #4CAF50; margin: 20px 0; color: #2E7D32; font-weight: 500;'>
                    Please upload an image of waste material for classification.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            try:
                # Open and convert image to RGB
                image = Image.open(uploaded_file).convert('RGB')
                
                # Display the image
                st.image(image, caption="Uploaded Image", use_container_width=True)
                
                if st.button("🔍 Classify Waste", use_container_width=True):
                    with st.spinner("🔄 Processing image..."):
                        # Preprocess the image
                        img_array = preprocess_image(image)
                        
                        if img_array is None:
                            st.error("Failed to preprocess image. Please try another image.")
                        else:
                            # Get prediction
                            prediction, confidence = predict_waste_class(st.session_state.model, img_array)
                            
                            if prediction is None:
                                st.error("Failed to classify image. Please try another image.")
                            else:
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                history_entry = {
                                    "timestamp": timestamp,
                                    "category": prediction,
                                    "confidence": float(confidence)
                                }
                                
                                # Add image data if available
                                if uploaded_file:
                                    try:
                                        history_entry["image"] = uploaded_file.getvalue()
                                        uploaded_file.seek(0)  # Reset file pointer for displaying
                                    except Exception as e:
                                        print(f"Error reading image data: {str(e)}")
                                
                                st.session_state.history.append(history_entry)
                                save_classification_history(history_entry)
                                
                                with col2:
                                    st.success("✅ Classification complete!")
                                    st.subheader("Results")
                                    
                                    st.markdown(f"""
                                    **Category:** {prediction.title()}  
                                    **Confidence:** {confidence:.1f}%
                                    """)
                                    
                                    st.progress(confidence / 100)
                                    
                                    st.subheader("Recycling Instructions")
                                    st.markdown(get_recycling_instructions(prediction))
                                    
                                    st.subheader("Characteristics")
                                    for char in waste_categories[prediction]["characteristics"]:
                                        st.markdown(f"✓ {char}")

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                print(f"Detailed error: {str(e)}")  # For debugging

# Recent classifications
if st.session_state.history:
    st.markdown("---")
    st.subheader("Recent Classifications")
    
    cols = st.columns(min(len(st.session_state.history[-3:]), 3))
    for col, entry in zip(cols, reversed(st.session_state.history[-3:])):
        with col:
            try:
                img = Image.open(io.BytesIO(entry["image"]))
                st.image(img, use_container_width=True)
                st.markdown(f"""
                **Category:** {entry['category'].title()}  
                **Confidence:** {entry['confidence']:.1f}%  
                {entry['timestamp']}
                """)
            except:
                st.markdown(f"""
                **Category:** {entry['category'].title()}  
                **Confidence:** {entry['confidence']:.1f}%  
                {entry['timestamp']}
                """)
