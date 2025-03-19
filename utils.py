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

# Create data directory in the same directory as the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
ensure_directory(DATA_DIR)

HISTORY_FILE = os.path.join(DATA_DIR, "classification_history.json")

def save_classification_history(entry):
    """Save a classification entry to history file"""
    try:
        # Create a copy of the entry to modify
        entry_to_save = entry.copy()
        
        # Convert image bytes to base64 string if it exists
        if "image" in entry_to_save and entry_to_save["image"] is not None:
            try:
                entry_to_save["image"] = base64.b64encode(entry_to_save["image"]).decode('utf-8')
            except Exception as e:
                print(f"Error encoding image: {str(e)}")
                # If image conversion fails, remove it from the entry
                del entry_to_save["image"]
        
        # Load existing history
        history = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                history = []
        
        # Add new entry
        history.append(entry_to_save)
        
        # Keep only last 10 entries
        history = history[-10:]
        
        # Save to file
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception as e:
        print(f"Error saving history: {str(e)}")
        st.error(f"Failed to save classification history: {str(e)}")

def get_classification_history():
    """Load classification history from file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                try:
                    history = json.load(f)
                    # Convert base64 strings back to bytes for display
                    for entry in history:
                        if "image" in entry and entry["image"] is not None:
                            try:
                                entry["image"] = base64.b64decode(entry["image"])
                            except:
                                # If image conversion fails, remove the image
                                del entry["image"]
                    return history
                except json.JSONDecodeError:
                    # If JSON is invalid, return empty list
                    return []
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
