import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About - Waste Classification System",
    page_icon="ℹ️",
    layout="wide"
)

# Hide only deploy button and unnecessary elements
st.markdown("""
    <style>
        .stDeployButton {display: none !important;}
        #MainMenu {visibility: hidden !important;}
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
st.title("ℹ️ About")

# Main content container
st.markdown("""
<div style='background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
""", unsafe_allow_html=True)

# Title and Introduction
st.header("Waste Classification System")
st.write("Welcome to our AI-powered Waste Classification System! This application helps you identify and properly dispose of different types of waste materials.")

# Features
st.subheader("✨ Features")
features = {
    "Image Classification": "Upload images of waste items for instant classification",
    "Recycling Guidance": "Get specific instructions for proper disposal",
    "Classification History": "Track your waste classification activities",
    "User-Friendly Interface": "Easy to use on any device"
}

for feature, desc in features.items():
    st.markdown(f"**{feature}:** {desc}")

# How It Works
st.subheader("🔄 How It Works")
steps = [
    "Upload an image of the waste item you want to classify",
    "Our AI model analyzes the image and identifies the type of waste",
    "Get instant results with recycling instructions",
    "View your classification history and track your recycling habits"
]

for i, step in enumerate(steps, 1):
    st.markdown(f"{i}. {step}")

# Supported Categories
st.subheader("📦 Supported Waste Categories")

# Create three columns for the categories
col1, col2 = st.columns(2)

categories = {
    "Cardboard": "Boxes, packaging materials",
    "Glass": "Bottles, jars, containers",
    "Metal": "Cans, aluminum items",
    "Paper": "Newspapers, documents",
    "Plastic": "Bottles, containers",
    "Trash": "Non-recyclable items"
}

# Split categories between columns
half = len(categories) // 2
for i, (category, desc) in enumerate(categories.items()):
    with col1 if i < half else col2:
        st.markdown(f"""
        <div style='background-color: #f1f8e9; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50; margin-bottom: 10px;'>
            <h4 style='color: #2E7D32; margin: 0;'>{category}</h4>
            <p style='margin: 5px 0 0 0; color: #666;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 30px; padding: 20px; color: #666;'>
    <p>Made with ❤️ for a cleaner environment</p>
</div>
""", unsafe_allow_html=True) 