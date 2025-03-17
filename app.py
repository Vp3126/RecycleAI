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
import tensorflow as tf

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

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state.history = []
if 'model' not in st.session_state:
    st.session_state.model = None

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
for category in waste_categories.keys():
    st.sidebar.markdown(f"- {category}")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Waste Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Classify button
            if st.button("Classify Waste"):
                with st.spinner("Processing image..."):
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
                    st.success(f"Classification complete!")
                    
                    with col2:
                        st.subheader("Classification Result")
                        st.markdown(f"**Category: {prediction}**")
                        st.progress(float(confidence))
                        st.markdown(f"Confidence: {confidence:.2f}%")
                        
                        st.subheader("Recycling Instructions")
                        instructions = get_recycling_instructions(prediction)
                        st.markdown(instructions)
                        
                        # Show characteristics of the waste category
                        st.subheader("Characteristics")
                        characteristics = waste_categories[prediction]["characteristics"]
                        for char in characteristics:
                            st.markdown(f"- {char}")
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

# Recent classifications
if st.session_state.history:
    st.markdown("---")
    st.subheader("Recent Classifications")
    
    # Display the last 3 classifications
    recent_history = st.session_state.history[-3:]
    recent_cols = st.columns(min(len(recent_history), 3))
    
    for i, (col, entry) in enumerate(zip(recent_cols, reversed(recent_history))):
        with col:
            try:
                img = Image.open(io.BytesIO(entry["image"]))
                st.image(img, width=150, caption=f"{entry['category']} ({entry['confidence']:.1f}%)")
            except:
                st.markdown(f"{entry['category']} ({entry['confidence']:.1f}%)")
            st.text(entry["timestamp"])

# Footer
st.markdown("---")
st.markdown("♻️ Waste Classification System - Powered by AI")
