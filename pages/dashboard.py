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

# Load custom CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Page title with styled heading
st.markdown('<h1 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">📊 Waste Classification Dashboard</h1>', unsafe_allow_html=True)

# Get history data
history = get_classification_history()
stats_by_category = get_stats_by_category()
stats_over_time = get_stats_over_time()

# Display overview metrics with styled container
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">📈 Overview</h2>', unsafe_allow_html=True)

if history:
    # Create a styled metrics container
    st.markdown('<div style="padding: 1rem; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Custom styled metric
        total = len(history)
        st.markdown(f'''
        <div style="text-align: center; padding: 1rem; background-color: #f1f8e9; border-radius: 8px; border-left: 5px solid #4CAF50;">
            <p style="margin-bottom: 5px; color: #555; font-size: 0.9rem;">Total Classifications</p>
            <h2 style="margin: 0; color: #2E7D32; font-size: 2rem;">{total}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        avg_confidence = np.mean([entry.get('confidence', 0) for entry in history])
        st.markdown(f'''
        <div style="text-align: center; padding: 1rem; background-color: #f1f8e9; border-radius: 8px; border-left: 5px solid #4CAF50;">
            <p style="margin-bottom: 5px; color: #555; font-size: 0.9rem;">Average Confidence</p>
            <h2 style="margin: 0; color: #2E7D32; font-size: 2rem;">{avg_confidence:.1f}%</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        if len(history) > 1:
            # Calculate classifications in last 24 hours
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            recent_count = sum(1 for entry in history if datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S") > yesterday)
        else:
            recent_count = 0
            
        st.markdown(f'''
        <div style="text-align: center; padding: 1rem; background-color: #f1f8e9; border-radius: 8px; border-left: 5px solid #4CAF50;">
            <p style="margin-bottom: 5px; color: #555; font-size: 0.9rem;">Recent (24h)</p>
            <h2 style="margin: 0; color: #2E7D32; font-size: 2rem;">{recent_count}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display classification distribution with styled container
    st.markdown('<div class="main-container" style="margin-top: 20px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">📊 Classification Distribution</h2>', unsafe_allow_html=True)
    
    if stats_by_category:
        # Prepare data for charts
        categories = [item['category'] for item in stats_by_category]
        counts = [item['count'] for item in stats_by_category]
        confidences = [item['avg_confidence'] for item in stats_by_category]
        
        # Create container for charts
        st.markdown('<div style="padding: 1rem; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Title for the chart container
            st.markdown('<h3 style="color: #2E7D32; text-align: center; font-size: 1.2rem;">Waste Type Distribution</h3>', unsafe_allow_html=True)
            # Create a pie chart for waste distribution with custom colors
            fig = px.pie(
                values=counts, 
                names=categories,
                color_discrete_sequence=['#4CAF50', '#8BC34A', '#CDDC39', '#FFC107', '#FF9800', '#FF5722']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Title for the chart container
            st.markdown('<h3 style="color: #2E7D32; text-align: center; font-size: 1.2rem;">Average Confidence by Waste Type</h3>', unsafe_allow_html=True)
            # Create a bar chart for confidence levels with custom colors
            fig = px.bar(
                x=categories, 
                y=confidences,
                labels={'x': 'Waste Type', 'y': 'Average Confidence (%)'},
                color_discrete_sequence=['#4CAF50']
            )
            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                xaxis=dict(title=''),
                yaxis=dict(title='Confidence (%)'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display classification over time with styled container
    st.markdown('</div>', unsafe_allow_html=True)  # Close previous container
    
    st.markdown('<div class="main-container" style="margin-top: 20px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">📈 Classifications Over Time</h2>', unsafe_allow_html=True)
    
    if not stats_over_time.empty:
        # Create container for the time chart
        st.markdown('<div style="padding: 1rem; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
        
        # Create a grouped bar chart for classifications over time with better styling
        fig = px.bar(
            stats_over_time, 
            x='date', 
            y='count',
            color='category',
            labels={'count': 'Number of Classifications', 'date': 'Date'},
            color_discrete_sequence=['#4CAF50', '#8BC34A', '#CDDC39', '#FFC107', '#FF9800', '#FF5722']
        )
        
        fig.update_layout(
            margin=dict(t=30, b=0, l=0, r=0),
            legend_title_text='Waste Category',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='',
                gridcolor='#eee',
            ),
            yaxis=dict(
                title='Number of Items',
                gridcolor='#eee',
            ),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Classification history table with styled container
    st.markdown('</div>', unsafe_allow_html=True)  # Close previous container
    
    st.markdown('<div class="main-container" style="margin-top: 20px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">📋 Classification History</h2>', unsafe_allow_html=True)
    
    if history:
        # Create container for the table
        st.markdown('<div style="padding: 1rem; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
        
        # Add a short description
        st.markdown('<p style="color: #666; margin-bottom: 15px;">Recent waste classifications with details:</p>', unsafe_allow_html=True)
        
        # Create a dataframe from the history
        df = pd.DataFrame(history)
        
        # Apply custom styles to the dataframe
        styled_df = df.style.format({
            'confidence': '{:.1f}%',
        })
        
        # Display the table with the most recent entries first
        st.dataframe(
            styled_df.sort_values('timestamp', ascending=False),
            use_container_width=True,
            height=300
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
else:
    st.info("No classification data available yet. Start classifying waste images to build your dashboard!")

# Footer with styled design
st.markdown('</div>', unsafe_allow_html=True)  # Close the last container

st.markdown('<footer class="footer">', unsafe_allow_html=True)
st.markdown('<div style="display: flex; justify-content: center; align-items: center; padding: 20px;">', unsafe_allow_html=True)
st.markdown('<span style="font-size: 1.2em; margin-right: 10px;">♻️</span> <span style="font-weight: bold; color: #2E7D32;">Waste Classification System</span> <span style="margin-left: 10px; color: #666;">Powered by AI</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</footer>', unsafe_allow_html=True)
