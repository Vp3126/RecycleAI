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

HISTORY_FILE = "classification_history.json"

def save_classification_history(entry):
    """Save a classification entry to history file"""
    try:
        # Convert image bytes to base64 string
        if "image" in entry:
            entry["image"] = base64.b64encode(entry["image"]).decode('utf-8')
        
        # Load existing history
        history = get_classification_history()
        
        # Add new entry
        history.append(entry)
        
        # Keep only last 10 entries
        history = history[-10:]
        
        # Save to file
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception as e:
        print(f"Error saving history: {str(e)}")

def get_classification_history():
    """Load classification history from file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                # Convert base64 strings back to bytes for display
                for entry in history:
                    if "image" in entry:
                        entry["image"] = base64.b64decode(entry["image"])
                return history
        return []
    except Exception as e:
        print(f"Error loading history: {str(e)}")
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
