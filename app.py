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

# Hide deploy button and other UI elements
st.markdown("""
    <style>
        .stDeployButton {display: none !important;}
        #MainMenu {visibility: hidden !important;}
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        .viewerBadge_container__1QSob {display: none !important;}
        div[data-testid="stToolbar"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# Add error handling for imports
try:
    from model import load_model, preprocess_image, predict_waste_class
    from utils import save_classification_history, get_classification_history
    from waste_info import waste_categories, get_recycling_instructions
except Exception as e:
    st.error(f"Error importing modules: {str(e)}")
    st.stop()

# Load custom CSS with error handling
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.warning("Could not load custom CSS. Using default styling.")
        # Add some basic CSS to make the app look decent
        st.markdown("""
            <style>
                .main-container { padding: 20px; }
                .sidebar-category { padding: 10px; margin: 5px 0; background-color: #f0f0f0; border-radius: 5px; }
                .sidebar-category:hover { background-color: #e0e0e0; }
                .classification-card { border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin: 10px 0; }
            </style>
        """, unsafe_allow_html=True)

load_css()

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

# App title
st.title("♻️ Waste Classification System")

# Load model with error handling
@st.cache_resource
def get_model():
    try:
        return load_model()
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
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

# Sidebar with error handling
try:
    st.sidebar.image("assets/recycle_logo.svg", width=100)
except:
    st.sidebar.markdown("♻️")

st.sidebar.title("Waste Classification")
st.sidebar.markdown("Upload an image of waste to classify it and get recycling guidance.")
st.sidebar.markdown("---")

# Categories in sidebar
st.sidebar.markdown("### Categories")
for category in waste_categories.keys():
    if st.sidebar.button(f"📦 {category.title()}", key=f"cat_{category}", use_container_width=True):
        st.session_state.selected_category = category
        st.rerun()

st.sidebar.markdown("---")

# Navigation
st.sidebar.markdown("### Navigation")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.selected_category = None
    st.rerun()

if st.sidebar.button("📊 Dashboard", use_container_width=True):
    st.switch_page("pages/dashboard.py")

if st.sidebar.button("📚 Education", use_container_width=True):
    st.switch_page("pages/education.py")

if st.sidebar.button("ℹ️ About", use_container_width=True):
    st.switch_page("pages/about.py")

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
        st.markdown('<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">Upload Waste Image</h2>', unsafe_allow_html=True)
        
        st.markdown('<p style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; border-left: 4px solid #4CAF50;">Please upload an image of waste material for classification.</p>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                if st.button("🔍 Classify Waste", use_container_width=True):
                    with st.spinner("🔄 Processing image..."):
                        img_array = preprocess_image(image)
                        prediction, confidence = predict_waste_class(st.session_state.model, img_array)
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        history_entry = {
                            "timestamp": timestamp,
                            "category": prediction,
                            "confidence": float(confidence),
                            "image": uploaded_file.getvalue()
                        }
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

# Recent classifications
if st.session_state.history:
    st.markdown("---")
    st.subheader("Recent Classifications")
    
    cols = st.columns(min(len(st.session_state.history[-3:]), 3))
    for col, entry in zip(cols, reversed(st.session_state.history[-3:])):
        with col:
            try:
                img = Image.open(io.BytesIO(entry["image"]))
                st.image(img, width=150)
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
