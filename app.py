import streamlit as st
import os
from PIL import Image
import io
from model import predict_waste
import time

# Set page config
st.set_page_config(
    page_title="RecycleAI - Waste Classification",
    page_icon="♻️",
    layout="wide",
    menu_items=None
)

# Add custom CSS
st.markdown("""
    <style>
    .stDeployButton {
        display: none;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("♻️ RecycleAI - Waste Classification")
st.markdown("""
    Upload an image of waste material, and our AI will help you identify its category and proper disposal method.
    This tool supports classification of plastic, glass, metal, paper, organic waste, and e-waste.
""")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Add a loading spinner
        with st.spinner("Analyzing image..."):
            # Add a small delay to show the spinner
            time.sleep(0.5)
            
            # Get prediction
            category, confidence = predict_waste(image)
            
            if category is None:
                st.error("Sorry, we couldn't process this image. Please try another one.")
            else:
                # Display results
                st.success(f"Classification: {category.title()}")
                st.metric("Confidence", f"{confidence:.2%}")
                
                # Display disposal information
                disposal_info = {
                    'plastic': "Recycle in designated plastic recycling bins. Clean and remove labels if possible.",
                    'glass': "Recycle in glass recycling bins. Handle with care to prevent breakage.",
                    'metal': "Recycle in metal recycling bins. Clean and remove any food residue.",
                    'paper': "Recycle in paper recycling bins. Remove any plastic or metal components.",
                    'organic': "Compost if possible, or dispose in organic waste bins.",
                    'e-waste': "Take to e-waste collection centers or electronics recycling facilities."
                }
                
                st.markdown("### Disposal Instructions")
                st.info(disposal_info.get(category, "Please check local recycling guidelines."))
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try uploading a different image.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ for a sustainable future</p>
        <p>© 2024 RecycleAI. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
