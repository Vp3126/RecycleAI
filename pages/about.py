import streamlit as st

st.set_page_config(
    page_title="About - Waste Classification System",
    page_icon="♻️",
    layout="wide"
)

# Load custom CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Styled container for the page content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Styled page title
st.markdown('<h1 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">About the Waste Classification System</h1>', unsafe_allow_html=True)

# Project Overview section with custom styling
st.markdown('''
<div class="info-card">
    <h2 style="color: #2E7D32; margin-bottom: 15px;">🌱 Project Overview</h2>
    
    <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;">
        The Waste Classification System is an AI-powered application that uses computer vision to identify different 
        types of waste materials from images. The system aims to promote proper waste sorting and recycling practices 
        by providing users with accurate classification and recycling guidance.
    </p>
</div>
''', unsafe_allow_html=True)

# How It Works section with custom styling
st.markdown('''
<div class="info-card" style="background-color: #f1f8e9; border-left: 5px solid #4CAF50; padding: 20px; border-radius: 10px; margin: 20px 0;">
    <h3 style="color: #2E7D32; margin-bottom: 15px;">🔄 How It Works</h3>
    
    <ol style="padding-left: 25px;">
        <li style="margin-bottom: 10px;"><strong>Image Upload</strong>: Users upload images of waste items they want to classify</li>
        <li style="margin-bottom: 10px;"><strong>AI Processing</strong>: Our trained machine learning model analyzes the image to identify the waste type</li>
        <li style="margin-bottom: 10px;"><strong>Classification</strong>: The system determines the category of waste (plastic, glass, metal, paper, organic, e-waste)</li>
        <li style="margin-bottom: 10px;"><strong>Guidance</strong>: Based on the classification, appropriate recycling or disposal instructions are provided</li>
    </ol>
</div>
''', unsafe_allow_html=True)

# Why It Matters section with custom styling
st.markdown('''
<div class="info-card">
    <h3 style="color: #2E7D32; margin-bottom: 15px;">🌍 Why It Matters</h3>
    
    <p style="font-size: 1.05rem; line-height: 1.5; margin-bottom: 15px;">
        Improper waste disposal and recycling contribute significantly to environmental problems:
    </p>
    
    <ul style="list-style-type: none; padding-left: 5px;">
        <li style="margin-bottom: 10px; display: flex; align-items: flex-start;">
            <span style="color: #F44336; margin-right: 10px;">⚠️</span> Landfills reaching capacity and leaching harmful chemicals
        </li>
        <li style="margin-bottom: 10px; display: flex; align-items: flex-start;">
            <span style="color: #F44336; margin-right: 10px;">⚠️</span> Ocean plastic pollution affecting marine life
        </li>
        <li style="margin-bottom: 10px; display: flex; align-items: flex-start;">
            <span style="color: #F44336; margin-right: 10px;">⚠️</span> Valuable resources being wasted instead of recycled
        </li>
        <li style="margin-bottom: 10px; display: flex; align-items: flex-start;">
            <span style="color: #F44336; margin-right: 10px;">⚠️</span> Increased carbon emissions from waste processing
        </li>
    </ul>
    
    <p style="font-size: 1.05rem; line-height: 1.5; margin-top: 15px; font-style: italic; border-left: 3px solid #4CAF50; padding-left: 15px;">
        By helping individuals correctly identify and properly dispose of waste, we can collectively make a positive environmental impact.
    </p>
</div>
''', unsafe_allow_html=True)

# Technology Stack section with custom styling
st.markdown('''
<div class="info-card" style="background-color: #e8f5e9; border-radius: 10px; padding: 20px; margin: 20px 0;">
    <h2 style="color: #2E7D32; margin-bottom: 15px;">💻 Technology Stack</h2>
    
    <p style="font-size: 1.05rem; margin-bottom: 15px;">This application is built using:</p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px;">
        <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <p style="font-weight: bold; margin-bottom: 5px;">Streamlit</p>
            <p style="font-size: 0.9rem; color: #666;">For the web application interface</p>
        </div>
        <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <p style="font-weight: bold; margin-bottom: 5px;">TensorFlow</p>
            <p style="font-size: 0.9rem; color: #666;">For the AI image classification model</p>
        </div>
        <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <p style="font-weight: bold; margin-bottom: 5px;">Python</p>
            <p style="font-size: 0.9rem; color: #666;">As the primary programming language</p>
        </div>
        <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <p style="font-weight: bold; margin-bottom: 5px;">OpenCV & Pillow</p>
            <p style="font-size: 0.9rem; color: #666;">For image processing</p>
        </div>
        <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <p style="font-weight: bold; margin-bottom: 5px;">Pandas</p>
            <p style="font-size: 0.9rem; color: #666;">For data handling and analytics</p>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Future Enhancements section with custom styling
st.markdown('''
<div class="info-card" style="margin: 20px 0;">
    <h2 style="color: #2E7D32; margin-bottom: 15px;">🚀 Future Enhancements</h2>
    
    <p style="font-size: 1.05rem; margin-bottom: 15px;">We plan to enhance the system with:</p>
    
    <ul style="list-style-type: none; padding-left: 5px;">
        <li style="margin-bottom: 10px; display: flex; align-items: flex-start;">
            <span style="color: #4CAF50; margin-right: 10px;">✅</span> Real-time waste classification using camera input
        </li>
        <li style="margin-bottom: 10px; display: flex; align-items: flex-start;">
            <span style="color: #4CAF50; margin-right: 10px;">✅</span> Community features for collaborative learning
        </li>
        <li style="margin-bottom: 10px; display: flex; align-items: flex-start;">
            <span style="color: #4CAF50; margin-right: 10px;">✅</span> Integration with local recycling facility information
        </li>
        <li style="margin-bottom: 10px; display: flex; align-items: flex-start;">
            <span style="color: #4CAF50; margin-right: 10px;">✅</span> Expanded waste categories and subcategories
        </li>
        <li style="margin-bottom: 10px; display: flex; align-items: flex-start;">
            <span style="color: #4CAF50; margin-right: 10px;">✅</span> Mobile application for on-the-go waste classification
        </li>
    </ul>
</div>
''', unsafe_allow_html=True)

# Feedback and Contributions section with custom styling
st.markdown('''
<div class="info-card" style="background-color: #f1f8e9; border-radius: 10px; padding: 20px; margin: 20px 0;">
    <h2 style="color: #2E7D32; margin-bottom: 15px;">📝 Feedback and Contributions</h2>
    
    <p style="font-size: 1.1rem; line-height: 1.6;">
        We welcome your feedback and contributions to improve the system. The project aims to be a valuable tool 
        in promoting environmental sustainability through proper waste management.
    </p>
</div>
''', unsafe_allow_html=True)

# Close the main container div
st.markdown('</div>', unsafe_allow_html=True)

# Footer with styled design
st.markdown('<footer class="footer">', unsafe_allow_html=True)
st.markdown('<div style="display: flex; justify-content: center; align-items: center; padding: 20px;">', unsafe_allow_html=True)
st.markdown('<span style="font-size: 1.2em; margin-right: 10px;">♻️</span> <span style="font-weight: bold; color: #2E7D32;">Waste Classification System</span> <span style="margin-left: 10px; color: #666;">Powered by AI</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</footer>', unsafe_allow_html=True)
