import numpy as np
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
    """
    Preprocess the image to match the model's expected input
    
    Args:
        image: PIL Image or file path
    
    Returns:
        Preprocessed image as numpy array
    """
    # Resize to expected dimensions
    if isinstance(image, str):
        image = Image.open(image)
    
    image = image.resize((224, 224))
    
    # Convert to numpy array and normalize
    img_array = np.array(image) / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_waste_class(model, image_array):
    """
    Predict waste class from image array
    
    Args:
        model: SimpleClassifier instance
        image_array: Preprocessed image as numpy array
    
    Returns:
        Tuple of (predicted_class, confidence)
    """
    # Get model prediction
    predictions = model.predict(image_array)
    
    # Get the index of the highest probability
    predicted_index = np.argmax(predictions)
    
    # Get the class name and confidence
    predicted_class = WASTE_CATEGORIES[predicted_index]
    confidence = predictions[predicted_index] * 100
    
    return predicted_class, confidence
