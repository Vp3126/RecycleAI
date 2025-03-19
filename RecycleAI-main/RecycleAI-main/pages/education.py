import streamlit as st
from waste_info import waste_categories

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
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.warning("Could not load custom CSS. Using default styling.")

load_css()

# Page title
st.title("📚 Waste Classification Education")

# Introduction
st.markdown("""
## Understanding Waste Classification

Proper waste classification is crucial for effective recycling and environmental protection. 
This guide will help you understand different types of waste and how to handle them correctly.
""")

# Display information for each category
for category, info in waste_categories.items():
    st.header(f"📦 {category.title()}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Description")
        st.write(info["description"])
        
        st.subheader("Characteristics")
        for char in info["characteristics"]:
            st.markdown(f"✓ {char}")
    
    with col2:
        st.subheader("Recycling Instructions")
        st.markdown(info["recycling_instructions"])
        
    st.markdown("---")

# Additional tips
st.header("💡 General Tips")
st.markdown("""
1. Always clean recyclable items before disposal
2. Remove any non-recyclable parts
3. Check local recycling guidelines
4. Keep recyclables dry and clean
5. Separate different types of waste
6. Reduce and reuse when possible
7. Compost organic waste
8. Handle hazardous waste with care
""")
