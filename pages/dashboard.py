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
        
        # First sort the original dataframe, then apply styling
        sorted_df = df.sort_values('timestamp', ascending=False)
        styled_df = sorted_df.style.format({
            'confidence': '{:.1f}%',
        })
        
        # Display the table with the most recent entries first
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=300
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add new Advanced Analytics section
        st.markdown('</div>', unsafe_allow_html=True)  # Close previous container
        
        st.markdown('<div class="main-container" style="margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;">🔍 Advanced Analytics</h2>', unsafe_allow_html=True)
        
        # Create container for advanced analytics
        st.markdown('<div style="padding: 1rem; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Waste Trends", "Environmental Impact", "Recycling Potential"])
        
        with tab1:
            st.markdown('<h3 style="color: #2E7D32; text-align: center; font-size: 1.2rem;">Waste Classification Trends</h3>', unsafe_allow_html=True)
            
            # Create a line chart for classification trends over time
            if not stats_over_time.empty:
                # Pivot the data to create time series for each category
                pivot_df = stats_over_time.pivot_table(index='date', columns='category', values='count', fill_value=0)
                
                # Plot line chart with plotly
                fig = px.line(
                    pivot_df, 
                    labels={'value': 'Number of Items', 'date': 'Date', 'variable': 'Waste Type'},
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
                
                # Add trend analysis text
                if len(pivot_df) > 1:
                    st.markdown('<div style="background-color: #f1f8e9; padding: 15px; border-radius: 8px; margin-top: 15px;">', unsafe_allow_html=True)
                    st.markdown('<h4 style="color: #2E7D32; font-size: 1.1rem; margin-bottom: 10px;">Trend Analysis</h4>', unsafe_allow_html=True)
                    
                    # Find most common waste type 
                    most_common = sorted(stats_by_category, key=lambda x: x['count'], reverse=True)[0]['category']
                    
                    st.markdown(f'''
                    <p style="margin-bottom: 8px;">• <strong>{most_common.title()}</strong> is the most commonly classified waste type.</p>
                    <p style="margin-bottom: 8px;">• Your waste classification activity is helping track recycling patterns.</p>
                    <p style="margin-bottom: 8px;">• Continue classifying to build more detailed trends over time.</p>
                    ''', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Start classifying waste to see trends over time!")
                
        with tab2:
            st.markdown('<h3 style="color: #2E7D32; text-align: center; font-size: 1.2rem;">Environmental Impact Metrics</h3>', unsafe_allow_html=True)
            
            if stats_by_category:
                # Create two columns for environmental impact
                impact_col1, impact_col2 = st.columns([1, 1])
                
                with impact_col1:
                    # Create gauge chart for recycling impact score
                    if len(history) > 0:
                        # Calculate recycling rate (simplified example)
                        recyclable_count = 0
                        for item in stats_by_category:
                            if item['category'] in ['plastic', 'glass', 'metal', 'paper']:
                                recyclable_count += item['count']
                        
                        total_count = sum(item['count'] for item in stats_by_category)
                        recycling_rate = (recyclable_count / total_count) * 100 if total_count > 0 else 0
                        
                        # Create gauge chart
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = recycling_rate,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Recycling Rate", 'font': {'size': 24, 'color': '#2E7D32'}},
                            gauge = {
                                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#2E7D32"},
                                'bar': {'color': "#2E7D32"},
                                'bgcolor': "white",
                                'borderwidth': 2,
                                'bordercolor': "#2E7D32",
                                'steps': [
                                    {'range': [0, 30], 'color': '#FFCDD2'},
                                    {'range': [30, 70], 'color': '#FFF9C4'},
                                    {'range': [70, 100], 'color': '#C8E6C9'}
                                ],
                            }
                        ))
                        
                        fig.update_layout(
                            height=250,
                            margin=dict(t=25, b=0, l=25, r=25),
                            paper_bgcolor='rgba(0,0,0,0)',
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                with impact_col2:
                    # Create a custom metric showing CO2 savings (simplified calculation)
                    if len(history) > 0:
                        # Example CO2 savings calculation (simplified for illustration)
                        # In a real app, you would use more accurate values based on waste type
                        plastic_count = sum(1 for entry in history if entry.get('category') == 'plastic')
                        glass_count = sum(1 for entry in history if entry.get('category') == 'glass')
                        metal_count = sum(1 for entry in history if entry.get('category') == 'metal')
                        paper_count = sum(1 for entry in history if entry.get('category') == 'paper')
                        
                        # Example savings factors (kg CO2 per item recycled)
                        co2_savings = plastic_count * 0.5 + glass_count * 0.3 + metal_count * 1.5 + paper_count * 0.2
                        trees_saved = paper_count * 0.1  # Example: 10 paper items = 1 tree
                        
                        st.markdown(f'''
                        <div style="background-color: #f1f8e9; padding: 15px; border-radius: 8px; text-align: center; height: 212px; display: flex; flex-direction: column; justify-content: center;">
                            <h4 style="color: #2E7D32; margin-bottom: 15px;">Estimated Environmental Impact</h4>
                            <div style="display: flex; justify-content: space-around;">
                                <div>
                                    <p style="font-size: 2rem; color: #2E7D32; margin: 0;">{co2_savings:.1f}kg</p>
                                    <p style="color: #555;">CO₂ Emissions Saved</p>
                                </div>
                                <div>
                                    <p style="font-size: 2rem; color: #2E7D32; margin: 0;">{trees_saved:.1f}</p>
                                    <p style="color: #555;">Trees Preserved</p>
                                </div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
            else:
                st.info("Start classifying waste to see environmental impact metrics!")
            
        with tab3:
            st.markdown('<h3 style="color: #2E7D32; text-align: center; font-size: 1.2rem;">Recycling Potential Analysis</h3>', unsafe_allow_html=True)
            
            if stats_by_category:
                # Create a more advanced stacked area chart for recycling potential by category
                if not stats_over_time.empty:
                    # Group data by recyclability
                    recyclable_categories = ['plastic', 'glass', 'metal', 'paper']
                    
                    # Prepare data for stacked chart
                    recycling_data = []
                    
                    for _, row in stats_over_time.iterrows():
                        is_recyclable = row['category'] in recyclable_categories
                        category_type = 'Recyclable' if is_recyclable else 'Non-recyclable'
                        recycling_data.append({
                            'date': row['date'],
                            'count': row['count'],
                            'category_type': category_type
                        })
                    
                    recycling_df = pd.DataFrame(recycling_data)
                    recycling_summary = recycling_df.groupby(['date', 'category_type']).sum().reset_index()
                    
                    # Create stacked area chart
                    fig = px.area(
                        recycling_summary, 
                        x="date", 
                        y="count", 
                        color="category_type",
                        labels={"count": "Number of Items", "date": "Date", "category_type": "Material Type"},
                        color_discrete_map={'Recyclable': '#4CAF50', 'Non-recyclable': '#FF5722'}
                    )
                    
                    fig.update_layout(
                        margin=dict(t=30, b=0, l=0, r=0),
                        legend_title_text='',
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
                    
                # Recycling opportunity breakdown
                recyclable_items = 0
                total_items = 0
                
                category_recycling = {}
                
                for item in stats_by_category:
                    category = item['category']
                    count = item['count']
                    total_items += count
                    
                    if category in ['plastic', 'glass', 'metal', 'paper']:
                        recyclable_items += count
                        category_recycling[category] = {
                            'count': count,
                            'recyclable': True,
                            'color': '#4CAF50'
                        }
                    else:
                        category_recycling[category] = {
                            'count': count,
                            'recyclable': False,
                            'color': '#FF5722'
                        }
                
                recycling_pct = (recyclable_items / total_items) * 100 if total_items > 0 else 0
                
                # Display recycling opportunity summary
                st.markdown(f'''
                <div style="background-color: #f1f8e9; padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <h4 style="color: #2E7D32; font-size: 1.1rem; margin-bottom: 10px;">Recycling Opportunity</h4>
                    <p style="margin-bottom: 10px;">
                        <span style="font-weight: bold; color: #2E7D32; font-size: 1.1rem;">{recycling_pct:.1f}%</span> 
                        of your classified waste items are recyclable.
                    </p>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.info("Start classifying waste to analyze recycling potential!")
            
        st.markdown('</div>', unsafe_allow_html=True)  # Close the advanced analytics container
    
else:
    st.info("No classification data available yet. Start classifying waste images to build your dashboard!")

# Footer with styled design
st.markdown('</div>', unsafe_allow_html=True)  # Close the last container

st.markdown('<footer class="footer">', unsafe_allow_html=True)
st.markdown('<div style="display: flex; justify-content: center; align-items: center; padding: 20px;">', unsafe_allow_html=True)
st.markdown('<span style="font-size: 1.2em; margin-right: 10px;">♻️</span> <span style="font-weight: bold; color: #2E7D32;">Waste Classification System</span> <span style="margin-left: 10px; color: #666;">Powered by AI</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</footer>', unsafe_allow_html=True)
