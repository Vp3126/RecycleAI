import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

from utils import get_classification_history, get_stats_by_category, get_stats_over_time

st.set_page_config(
    page_title="Dashboard - Waste Classification System",
    page_icon="♻️",
    layout="wide"
)

st.title("Waste Classification Dashboard")

# Get history data
history = get_classification_history()
stats_by_category = get_stats_by_category()
stats_over_time = get_stats_over_time()

# Display overview metrics
st.subheader("Overview")

if history:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Classifications", len(history))
    
    with col2:
        avg_confidence = np.mean([entry.get('confidence', 0) for entry in history])
        st.metric("Average Confidence", f"{avg_confidence:.1f}%")
    
    with col3:
        if len(history) > 1:
            # Calculate classifications in last 24 hours
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            recent_count = sum(1 for entry in history if datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S") > yesterday)
            st.metric("Recent (24h)", recent_count)
        else:
            st.metric("Recent (24h)", 0)
    
    # Display classification distribution
    st.subheader("Classification Distribution")
    
    if stats_by_category:
        # Prepare data for charts
        categories = [item['category'] for item in stats_by_category]
        counts = [item['count'] for item in stats_by_category]
        confidences = [item['avg_confidence'] for item in stats_by_category]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create a pie chart for waste distribution
            fig = px.pie(
                values=counts, 
                names=categories,
                title='Waste Type Distribution',
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Create a bar chart for confidence levels
            fig = px.bar(
                x=categories, 
                y=confidences,
                title='Average Confidence by Waste Type',
                labels={'x': 'Waste Type', 'y': 'Average Confidence (%)'},
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Display classification over time
    st.subheader("Classifications Over Time")
    
    if not stats_over_time.empty:
        # Create a grouped bar chart for classifications over time
        fig = px.bar(
            stats_over_time, 
            x='date', 
            y='count',
            color='category',
            title='Daily Classifications by Waste Type',
            labels={'count': 'Number of Classifications', 'date': 'Date'},
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Classification history table
    st.subheader("Classification History")
    
    if history:
        # Create a dataframe from the history
        df = pd.DataFrame(history)
        
        # Display the table with the most recent entries first
        st.dataframe(df.sort_values('timestamp', ascending=False), use_container_width=True)
    
else:
    st.info("No classification data available yet. Start classifying waste images to build your dashboard!")

st.markdown("---")
st.markdown("♻️ Waste Classification System - Powered by AI")
