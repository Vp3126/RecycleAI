import numpy as np
from PIL import Image
import io

class SimpleClassifier:
    """
    A simple classifier for testing purposes
    """
    def __init__(self):
        self.categories = ['plastic', 'glass', 'metal', 'paper', 'organic', 'e-waste']
    
    def predict(self, image_array):
        # For testing, return random predictions
        predictions = np.random.random(6)
        predictions = predictions / np.sum(predictions)
        return predictions

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
    predicted_class = model.categories[predicted_index]
    confidence = predictions[predicted_index] * 100
    
    return predicted_class, confidence
