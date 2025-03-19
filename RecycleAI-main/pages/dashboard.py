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

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Dashboard - Waste Classification System",
    page_icon="📊",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS
st.markdown("""
    <style>
        .stDeployButton {display: none !important;}
        #MainMenu {visibility: hidden !important;}
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        .viewerBadge_container__1QSob {display: none !important;}
        div[data-testid="stToolbar"] {display: none !important;}
        
        /* Dashboard styling */
        .dashboard-container {
            padding: 2rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .metric-card {
            text-align: center;
            padding: 1.5rem;
            background-color: #f1f8e9;
            border-radius: 8px;
            border-left: 5px solid #4CAF50;
            margin-bottom: 15px;
        }
        
        .metric-card p {
            margin-bottom: 5px;
            color: #555;
            font-size: 0.9rem;
        }
        
        .metric-card h2 {
            margin: 0;
            color: #2E7D32;
            font-size: 2rem;
        }
        
        /* Chart containers */
        .chart-container {
            padding: 1.5rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #2E7D32;
            margin-bottom: 1rem;
        }
        
        /* Progress bars */
        .stProgress > div > div {
            background-color: #4CAF50;
        }
    </style>
""", unsafe_allow_html=True)

# Page title with styled heading
st.markdown('<h1 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">📊 Waste Classification Dashboard</h1>', unsafe_allow_html=True)

# Get history data
try:
    history = get_classification_history()
    stats_by_category = get_stats_by_category()
    stats_over_time = get_stats_over_time()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    history = []
    stats_by_category = []
    stats_over_time = pd.DataFrame()

# Display overview metrics
st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
st.markdown('<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">📈 Overview</h2>', unsafe_allow_html=True)

if history:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total = len(history)
        st.markdown(f'''
        <div class="metric-card">
            <p>Total Classifications</p>
            <h2>{total}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        avg_confidence = np.mean([entry.get('confidence', 0) for entry in history])
        st.markdown(f'''
        <div class="metric-card">
            <p>Average Confidence</p>
            <h2>{avg_confidence:.1f}%</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        recent_count = sum(1 for entry in history if datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S") > yesterday)
        st.markdown(f'''
        <div class="metric-card">
            <p>Recent (24h)</p>
            <h2>{recent_count}</h2>
        </div>
        ''', unsafe_allow_html=True)

    # Charts section
    if stats_by_category:
        st.markdown('<h2 style="color: #2E7D32; margin-top: 2rem;">Classification Distribution</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            categories = [item['category'] for item in stats_by_category]
            counts = [item['count'] for item in stats_by_category]
            
            fig = px.pie(
                values=counts,
                names=categories,
                title="Waste Type Distribution",
                color_discrete_sequence=['#4CAF50', '#8BC34A', '#CDDC39', '#FFC107', '#FF9800', '#FF5722']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            confidences = [item['avg_confidence'] for item in stats_by_category]
            
            fig = px.bar(
                x=categories,
                y=confidences,
                title="Average Confidence by Waste Type",
                labels={'x': 'Waste Type', 'y': 'Confidence (%)'},
                color_discrete_sequence=['#4CAF50']
            )
            st.plotly_chart(fig, use_container_width=True)

    # History table
    st.markdown('<h2 style="color: #2E7D32; margin-top: 2rem;">Recent Classifications</h2>', unsafe_allow_html=True)
    
    if len(history) > 0:
        df = pd.DataFrame(history)
        df = df.sort_values('timestamp', ascending=False)
        st.dataframe(
            df,
            use_container_width=True,
            height=300
        )
    else:
        st.info("No classification history available yet. Start classifying waste to see your history!")

else:
    st.info("No data available yet. Start classifying waste to build your dashboard!")

st.markdown('</div>', unsafe_allow_html=True)
