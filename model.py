import tensorflow as tf
import numpy as np
import os
from PIL import Image
import io
import random

# Define waste categories
WASTE_CATEGORIES = [
    "plastic", 
    "glass", 
    "metal", 
    "paper", 
    "organic", 
    "e-waste"
]

# Define the model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'waste_classifier.h5')

# Load the model once at startup
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class SimpleClassifier:
    """
    A simple classifier that simulates AI predictions without using TensorFlow
    """
    def __init__(self):
        self.categories = WASTE_CATEGORIES
        self.ready = True
        
    def predict(self, image_array):
        """
        Simulates prediction based on image features
        """
        # Extract simple features from the image (average color values)
        if len(image_array.shape) == 4:  # Handle batch dimension
            image_array = image_array[0]
            
        # Calculate average color values per channel
        avg_colors = np.mean(image_array, axis=(0, 1))
        
        # Use colors to influence the prediction (just for simulation)
        # This is not real ML but allows the app to function without TensorFlow
        r, g, b = avg_colors
        
        # Create prediction probabilities influenced by color values
        # This is simplified and for demonstration only
        probs = np.zeros(len(self.categories))
        
        # High red content could indicate plastic or metal
        probs[0] += r * 0.5  # plastic
        probs[2] += r * 0.3  # metal
        
        # High green content could indicate organic or paper
        probs[3] += g * 0.4  # paper
        probs[4] += g * 0.6  # organic
        
        # High blue content could indicate glass or e-waste
        probs[1] += b * 0.5  # glass
        probs[5] += b * 0.4  # e-waste
        
        # Add some randomness to make it interesting
        probs += np.random.random(len(probs)) * 0.4
        
        # Normalize to sum to 1
        probs = probs / np.sum(probs)
        
        return probs

def load_model():
    """
    Load or create a waste classification model
    """
    # Create a simple classifier instead of a TensorFlow model
    model = SimpleClassifier()
    return model

def preprocess_image(image):
    """Preprocess the image for model input."""
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize((224, 224))
        
        # Convert to array and preprocess
        img_array = np.array(image)
        img_array = img_array / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_waste(image):
    """Predict waste category from image."""
    try:
        if model is None:
            return None, "Error: Model not loaded"
            
        # Preprocess image
        processed_image = preprocess_image(image)
        if processed_image is None:
            return None, "Error: Image preprocessing failed"
        
        # Make prediction
        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction[0])
        confidence = float(prediction[0][predicted_class])
        
        # Map class index to category
        categories = ['plastic', 'glass', 'metal', 'paper', 'organic', 'e-waste']
        category = categories[predicted_class]
        
        return category, confidence
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None, "Error: Prediction failed"
