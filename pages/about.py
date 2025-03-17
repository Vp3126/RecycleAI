import streamlit as st

st.set_page_config(
    page_title="About - Waste Classification System",
    page_icon="♻️",
    layout="wide"
)

st.title("About the Waste Classification System")

st.markdown("""
## Project Overview

The Waste Classification System is an AI-powered application that uses computer vision to identify different types of waste materials from images. The system aims to promote proper waste sorting and recycling practices by providing users with accurate classification and recycling guidance.

### How It Works

1. **Image Upload**: Users upload images of waste items they want to classify
2. **AI Processing**: Our trained machine learning model analyzes the image to identify the waste type
3. **Classification**: The system determines the category of waste (plastic, glass, metal, paper, organic, e-waste)
4. **Guidance**: Based on the classification, appropriate recycling or disposal instructions are provided

### Why It Matters

Improper waste disposal and recycling contribute significantly to environmental problems:

- Landfills reaching capacity and leaching harmful chemicals
- Ocean plastic pollution affecting marine life
- Valuable resources being wasted instead of recycled
- Increased carbon emissions from waste processing

By helping individuals correctly identify and properly dispose of waste, we can collectively make a positive environmental impact.

## Technology Stack

This application is built using:

- **Streamlit**: For the web application interface
- **TensorFlow**: For the AI image classification model
- **Python**: As the primary programming language
- **OpenCV & Pillow**: For image processing
- **Pandas**: For data handling and analytics

## Future Enhancements

We plan to enhance the system with:

- Real-time waste classification using camera input
- Community features for collaborative learning
- Integration with local recycling facility information
- Expanded waste categories and subcategories
- Mobile application for on-the-go waste classification

## Feedback and Contributions

We welcome your feedback and contributions to improve the system. The project aims to be a valuable tool in promoting environmental sustainability through proper waste management.
""")

st.markdown("---")
st.markdown("♻️ Waste Classification System - Powered by AI")
