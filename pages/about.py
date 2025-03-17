import streamlit as st

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="About - Waste Classification System",
    page_icon="♻️",
    layout="wide",
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

# App title
st.title("♻️ About the Waste Classification System")

# Project Overview section
st.header("🌱 Project Overview")
st.write("""
The Waste Classification System is an AI-powered application that uses computer vision to identify different 
types of waste materials from images. The system aims to promote proper waste sorting and recycling practices 
by providing users with accurate classification and recycling guidance.
""")

# How It Works section
st.header("🔄 How It Works")
st.markdown("""
1. **Image Upload**: Users upload images of waste items they want to classify
2. **AI Processing**: Our trained machine learning model analyzes the image to identify the waste type
3. **Classification**: The system determines the category of waste (plastic, glass, metal, paper, organic, e-waste)
4. **Guidance**: Based on the classification, appropriate recycling or disposal instructions are provided
""")

# Why It Matters section
st.header("🌍 Why It Matters")
st.write("""
Improper waste disposal and recycling contribute significantly to environmental problems:
""")

st.markdown("""
- ⚠️ Landfills reaching capacity and leaching harmful chemicals
- ⚠️ Ocean plastic pollution affecting marine life
- ⚠️ Valuable resources being wasted instead of recycled
- ⚠️ Increased carbon emissions from waste processing
""")

st.info("""
By helping individuals correctly identify and properly dispose of waste, we can collectively make a positive environmental impact.
""")

# Technology Stack section
st.header("💻 Technology Stack")
st.write("This application is built using:")

tech_cols = st.columns(5)
with tech_cols[0]:
    st.markdown("""
    **Streamlit**  
    For the web application interface
    """)

with tech_cols[1]:
    st.markdown("""
    **TensorFlow**  
    For the AI image classification model
    """)

with tech_cols[2]:
    st.markdown("""
    **Python**  
    As the primary programming language
    """)

with tech_cols[3]:
    st.markdown("""
    **OpenCV & Pillow**  
    For image processing
    """)

with tech_cols[4]:
    st.markdown("""
    **Pandas**  
    For data handling and analytics
    """)

# Future Enhancements section
st.header("🚀 Future Enhancements")
st.write("We plan to enhance the system with:")

st.markdown("""
- ✅ Real-time waste classification using camera input
- ✅ Community features for collaborative learning
- ✅ Integration with local recycling facility information
- ✅ Expanded waste categories and subcategories
- ✅ Mobile application for on-the-go waste classification
""")

# Feedback and Contributions section
st.header("📝 Feedback and Contributions")
st.write("""
We welcome your feedback and contributions to improve the system. The project aims to be a valuable tool 
in promoting environmental sustainability through proper waste management.
""")
