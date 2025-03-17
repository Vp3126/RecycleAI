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

from model import load_model, preprocess_image, predict_waste_class
from utils import save_classification_history, get_classification_history
from waste_info import waste_categories, get_recycling_instructions

# Page configuration
st.set_page_config(
    page_title="Waste Classification System",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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

# Load model
@st.cache_resource
def get_model():
    return load_model()

# Try to load the model
try:
    if st.session_state.model is None:
        with st.spinner("Loading AI model..."):
            st.session_state.model = get_model()
        st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading model: {str(e)}")

# Sidebar
st.sidebar.image("assets/recycle_logo.svg", width=100)
st.sidebar.title("Waste Classification")
st.sidebar.markdown("Upload an image of waste to classify it and get recycling guidance.")
st.sidebar.markdown("---")
st.sidebar.markdown("### Categories")

# Enhanced sidebar categories with hover effect and links
for category in waste_categories.keys():
    category_html = f"""
    <a href="?category={category}" class="sidebar-category-link">
        <div class="sidebar-category">
            <span>{category}</span>
        </div>
    </a>
    """
    st.sidebar.markdown(category_html, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
nav_html = """
<a href="/" class="sidebar-category-link">
    <div class="sidebar-category">
        <span>🏠 Home</span>
    </div>
</a>
<a href="/Dashboard" class="sidebar-category-link">
    <div class="sidebar-category">
        <span>📊 Dashboard</span>
    </div>
</a>
<a href="/Education" class="sidebar-category-link">
    <div class="sidebar-category">
        <span>📚 Education</span>
    </div>
</a>
<a href="/About" class="sidebar-category-link">
    <div class="sidebar-category">
        <span>ℹ️ About</span>
    </div>
</a>
"""
st.sidebar.markdown(nav_html, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Check if a category is selected from the sidebar
if st.session_state.selected_category and st.session_state.selected_category in waste_categories:
    selected_category = st.session_state.selected_category
    
    st.markdown(f'<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">{selected_category}</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Display category information
        st.markdown(f'<h3 style="color: #2E7D32;">About {selected_category}</h3>', unsafe_allow_html=True)
        st.markdown(f'<div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0;">{waste_categories[selected_category]["description"]}</div>', unsafe_allow_html=True)
        
        # Show characteristics
        st.markdown(f'<h3 style="color: #2E7D32; margin-top: 20px;">Characteristics</h3>', unsafe_allow_html=True)
        characteristics_html = '<div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0;">'
        for char in waste_categories[selected_category]["characteristics"]:
            characteristics_html += f'<div style="padding: 5px 10px; margin-bottom: 5px; background-color: #f1f8e9; border-radius: 5px;">✓ {char}</div>'
        characteristics_html += '</div>'
        st.markdown(characteristics_html, unsafe_allow_html=True)
    
    with col2:
        # Display recycling instructions
        st.markdown(f'<h3 style="color: #2E7D32;">Recycling Instructions</h3>', unsafe_allow_html=True)
        instructions = get_recycling_instructions(selected_category)
        st.markdown(f'<div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0;">{instructions}</div>', unsafe_allow_html=True)
        
        # Button to clear selection
        st.markdown('<div style="display: flex; justify-content: center; margin: 20px 0;">', unsafe_allow_html=True)
        if st.button("🔙 Back to Home"):
            st.session_state.selected_category = None
            # Clear query parameters
            for param in st.query_params:
                del st.query_params[param]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Regular upload interface when no category is selected
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">Upload Waste Image</h2>', unsafe_allow_html=True)
        
        # Styled file uploader instruction
        st.markdown('<p style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; border-left: 4px solid #4CAF50;">Please upload an image of waste material for classification.</p>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded image with a styled container
            image = Image.open(uploaded_file)
            st.markdown('<div style="padding: 10px; border-radius: 10px; border: 1px solid #e0e0e0;">', unsafe_allow_html=True)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Fancy classify button
            button_container = st.container()
            with button_container:
                st.markdown('<div style="display: flex; justify-content: center; margin: 20px 0;">', unsafe_allow_html=True)
                classify_btn = st.button("🔍 Classify Waste")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if classify_btn:
                with st.spinner("🔄 Processing image..."):
                    # Preprocess image
                    img_array = preprocess_image(image)
                    
                    # Make prediction
                    prediction, confidence = predict_waste_class(st.session_state.model, img_array)
                    
                    # Record in history
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    history_entry = {
                        "timestamp": timestamp,
                        "category": prediction,
                        "confidence": float(confidence),
                        "image": uploaded_file.getvalue()
                    }
                    st.session_state.history.append(history_entry)
                    save_classification_history(history_entry)
                    
                    # Show classification result
                    st.success(f"✅ Classification complete!")
                    
                    with col2:
                        st.markdown(f'<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">Classification Result</h2>', unsafe_allow_html=True)
                        
                        result_html = f"""
                        <div style="background-color: #f1f8e9; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #4CAF50;">
                            <h3 style="margin-top: 0; color: #2E7D32;">Category: {prediction}</h3>
                            <p>Confidence: {confidence:.2f}%</p>
                        </div>
                        """
                        st.markdown(result_html, unsafe_allow_html=True)
                        st.progress(float(confidence/100))
                        
                        st.markdown(f'<h3 style="color: #2E7D32; margin-top: 30px;">Recycling Instructions</h3>', unsafe_allow_html=True)
                        instructions = get_recycling_instructions(prediction)
                        st.markdown(f'<div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0;">{instructions}</div>', unsafe_allow_html=True)
                        
                        # Show characteristics of the waste category
                        st.markdown(f'<h3 style="color: #2E7D32; margin-top: 30px;">Characteristics</h3>', unsafe_allow_html=True)
                        
                        characteristics_html = '<div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0;">'
                        for char in waste_categories[prediction]["characteristics"]:
                            characteristics_html += f'<div style="padding: 5px 10px; margin-bottom: 5px; background-color: #f1f8e9; border-radius: 5px;">✓ {char}</div>'
                        characteristics_html += '</div>'
                        
                        st.markdown(characteristics_html, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Recent classifications
if st.session_state.history:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px; margin-top: 20px;">Recent Classifications</h2>', unsafe_allow_html=True)
    
    # Display the last 3 classifications
    recent_history = st.session_state.history[-3:]
    recent_cols = st.columns(min(len(recent_history), 3))
    
    for i, (col, entry) in enumerate(zip(recent_cols, reversed(recent_history))):
        with col:
            try:
                st.markdown('<div class="classification-card">', unsafe_allow_html=True)
                img = Image.open(io.BytesIO(entry["image"]))
                st.image(img, width=150, caption="")
                
                # Card content
                card_content = f"""
                <div style="padding: 10px 5px;">
                    <h4 style="margin: 0; color: #2E7D32; text-align: center;">{entry['category']}</h4>
                    <div style="background-color: #f1f8e9; height: 10px; border-radius: 5px; margin: 8px 0;">
                        <div style="background-color: #4CAF50; width: {entry['confidence']}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                    <p style="margin: 0; text-align: center; font-size: 0.9em; color: #666;">Confidence: {entry['confidence']:.1f}%</p>
                    <p style="margin: 5px 0 0; text-align: center; font-size: 0.8em; color: #888;">{entry["timestamp"]}</p>
                </div>
                """
                st.markdown(card_content, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            except:
                st.markdown(f'<div class="classification-card"><h4>{entry["category"]}</h4><p>Confidence: {entry["confidence"]:.1f}%</p><p>{entry["timestamp"]}</p></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
# st.markdown('<footer class="footer">', unsafe_allow_html=True)
# st.markdown('<div style="display: flex; justify-content: center; align-items: center; padding: 20px;">', unsafe_allow_html=True)
# st.markdown('<span style="font-size: 1.2em; margin-right: 10px;">♻️</span> <span style="font-weight: bold; color: #2E7D32;">Waste Classification System</span> <span style="margin-left: 10px; color: #666;">Powered by AI</span>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)
# st.markdown('</footer>', unsafe_allow_html=True)
