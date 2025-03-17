import json
import os
import io
import base64
from datetime import datetime
import pandas as pd
import streamlit as st

# Create directory for storing classification history
def ensure_directory(directory):
    """Ensure that a directory exists, create if it doesn't"""
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create data directory
ensure_directory("data")

def save_classification_history(entry):
    """
    Save classification history to a JSON file
    
    Args:
        entry: Dictionary containing classification details
    """
    history_file = "data/classification_history.csv"
    
    # Convert image to base64 to save as string
    if "image" in entry:
        image_bytes = entry["image"]
        del entry["image"]  # Remove actual bytes before saving
        
    # Create DataFrame from entry
    df_entry = pd.DataFrame([entry])
    
    # Append to CSV or create new file
    if os.path.exists(history_file):
        df_entry.to_csv(history_file, mode='a', header=False, index=False)
    else:
        df_entry.to_csv(history_file, index=False)
    
    return True

def get_classification_history():
    """
    Get classification history from saved JSON file
    
    Returns:
        List of classification history entries
    """
    history_file = "data/classification_history.csv"
    
    if os.path.exists(history_file):
        history_df = pd.read_csv(history_file)
        return history_df.to_dict('records')
    
    return []

def get_stats_by_category():
    """
    Get statistics by waste category
    
    Returns:
        Dictionary with category counts and average confidence
    """
    history = get_classification_history()
    
    if not history:
        return {}
    
    # Convert to DataFrame for easy analysis
    df = pd.DataFrame(history)
    
    # Group by category
    stats = df.groupby('category').agg(
        count=('category', 'count'),
        avg_confidence=('confidence', 'mean')
    ).reset_index()
    
    return stats.to_dict('records')

def get_stats_over_time():
    """
    Get statistics over time
    
    Returns:
        DataFrame with daily counts
    """
    history = get_classification_history()
    
    if not history:
        return pd.DataFrame()
    
    # Convert to DataFrame for easy analysis
    df = pd.DataFrame(history)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # Group by date
    stats = df.groupby(['date', 'category']).agg(
        count=('category', 'count')
    ).reset_index()
    
    return stats
