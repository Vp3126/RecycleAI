import streamlit as st
from waste_info import waste_categories
import os

# Get the directory where education.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)  # Parent directory of pages

# Page configuration
st.set_page_config(
    page_title="Education - Waste Classification System",
    page_icon="📚",
    layout="wide"
)

# Hide deploy menu and other UI elements
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

# Load CSS
def load_css():
    try:
        css_path = os.path.join(ROOT_DIR, "style.css")
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

load_css()

# Page title
st.title("📚 Waste Classification Education")

# Introduction
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <h2 style='color: #2E7D32;'>Understanding Waste Classification</h2>
    <p style='color: #333333;'>
        Proper waste classification is crucial for effective recycling and environmental protection.<br>
        This guide will help you understand different types of waste and how to handle them correctly.
    </p>
</div>
""", unsafe_allow_html=True)

# Display information for each category
for category, info in waste_categories.items():
    st.markdown(f"""
    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h2 style='color: #2E7D32;'>📦 {category.title()}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style='background-color: #f1f8e9; padding: 15px; border-radius: 8px; margin-bottom: 15px;'>
            <h3 style='color: #2E7D32;'>Description</h3>
            <p style='color: #333333;'>
        """, unsafe_allow_html=True)
        st.write(info["description"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: #1b5e20; padding: 15px; border-radius: 8px;'>
            <h3 style='color: white;'>Characteristics</h3>
        """, unsafe_allow_html=True)
        for char in info["characteristics"]:
            st.markdown(f"<p style='color: white; margin: 8px 0;'>✓ {char}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #f1f8e9; padding: 15px; border-radius: 8px;'>
            <h3 style='color: #2E7D32;'>Recycling Instructions</h3>
            <div style='color: #333333;'>
        """, unsafe_allow_html=True)
        st.markdown(info["recycling_instructions"])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
    st.markdown("<hr style='margin: 30px 0; border-color: #4CAF50;'>", unsafe_allow_html=True)

# Additional tips
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
    <h2 style='color: #2E7D32;'>💡 General Tips</h2>
    <div style='color: #333333;'>
        1. Always clean recyclable items before disposal<br>
        2. Remove any non-recyclable parts<br>
        3. Check local recycling guidelines<br>
        4. Keep recyclables dry and clean<br>
        5. Separate different types of waste<br>
        6. Reduce and reuse when possible<br>
        7. Compost organic waste<br>
        8. Handle hazardous waste with care
    </div>
</div>
""", unsafe_allow_html=True)
