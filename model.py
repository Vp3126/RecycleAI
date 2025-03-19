import torch
import torch.nn as nn
import torchvision.models as models
from PIL import Image
import io
import cv2
import numpy as np
import os
from torchvision import transforms

# Define waste categories globally
WASTE_CATEGORIES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Get the directory where model.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class WasteClassifier:
    """
    A classifier that uses image features for waste classification
    """
    def __init__(self):
        self.categories = WASTE_CATEGORIES
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._create_model()
    
    def _create_model(self):
        # Load pre-trained ResNet50
        model = models.resnet50(pretrained=True)
        
        # Modify the final layer for our 6 classes
        num_features = model.fc.in_features
        model.fc = nn.Linear(num_features, len(self.categories))
        
        return model.to(self.device)
    
    def load_weights(self, weights_path):
        """Load trained weights"""
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Model weights not found at: {weights_path}")
        print(f"Loading model weights from: {weights_path}")
        state_dict = torch.load(weights_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()
    
    def predict(self, image_tensor):
        """Predict using the deep learning model"""
        try:
            # Move to device
            image_tensor = image_tensor.to(self.device)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                probabilities = probabilities.cpu().numpy()[0]
            
            return probabilities
        except Exception as e:
            print(f"Error in model prediction: {str(e)}")
            return None

def load_model(model_path=None):
    """
    Load the waste classification model
    Args:
        model_path: Optional path to the model weights file. If not provided, will look in default locations.
    Returns:
        WasteClassifier instance or None if loading fails
    """
    try:
        if model_path is None:
            # Try default locations
            model_path = os.path.join(SCRIPT_DIR, 'waste_model.pth')
            if not os.path.exists(model_path):
                # Try one directory up
                model_path = os.path.join(os.path.dirname(SCRIPT_DIR), 'waste_model.pth')
        
        print(f"Attempting to load model from: {model_path}")
        if not os.path.exists(model_path):
            print(f"Model file not found at: {model_path}")
            return None
            
        classifier = WasteClassifier()
        classifier.load_weights(model_path)
        print("Model loaded successfully!")
        return classifier
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None

def preprocess_image(image):
    try:
        # Convert PIL Image to RGB if it's not
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Define the preprocessing transforms
        preprocess = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Apply preprocessing
        img_tensor = preprocess(image)
        
        # Add batch dimension
        img_tensor = img_tensor.unsqueeze(0)
        
        return img_tensor
    except Exception as e:
        print(f"Error preprocessing image: {str(e)}")
        return None

def predict_waste_class(model, image_tensor):
    try:
        if model is None or image_tensor is None:
            print("Model or image tensor is None")
            return None, 0.0
            
        # Get probabilities from model
        probabilities = model.predict(image_tensor)
        if probabilities is None:
            print("Failed to get probabilities from model")
            return None, 0.0
            
        # Get top 3 predictions for debugging
        top3_indices = np.argsort(probabilities)[-3:][::-1]
        top3_probabilities = probabilities[top3_indices]
        
        # Print top 3 predictions for debugging
        print("\nTop 3 predictions:")
        for i in range(3):
            idx = top3_indices[i]
            prob = top3_probabilities[i] * 100
            print(f"{WASTE_CATEGORIES[idx]}: {prob:.2f}%")
        
        # Get the highest probability prediction
        predicted_idx = np.argmax(probabilities)
        confidence = probabilities[predicted_idx] * 100
        predicted_category = WASTE_CATEGORIES[predicted_idx]
        
        # Special handling for plastic items
        plastic_idx = WASTE_CATEGORIES.index('plastic')
        paper_idx = WASTE_CATEGORIES.index('paper')
        
        # If the prediction is paper and plastic is in top 2 with decent confidence
        if predicted_category == 'paper' and confidence < 70:
            # Check if plastic is in top 2 predictions
            for i in range(2):
                if top3_indices[i] == plastic_idx:
                    plastic_prob = top3_probabilities[i] * 100
                    if plastic_prob > 35:
                        predicted_category = 'plastic'
                        confidence = plastic_prob
                        break
        
        # If confidence is too low, try to use the second best prediction
        elif confidence < 45 and top3_probabilities[1] * 100 > 35:
            # If the second best prediction is glass or plastic, use it
            second_best_idx = top3_indices[1]
            second_best_category = WASTE_CATEGORIES[second_best_idx]
            if second_best_category in ['glass', 'plastic']:
                predicted_category = second_best_category
                confidence = top3_probabilities[1] * 100
        
        # Additional check for plastic items
        if predicted_category == 'paper' and confidence < 80:
            plastic_prob = probabilities[plastic_idx] * 100
            if plastic_prob > 40:
                predicted_category = 'plastic'
                confidence = plastic_prob
        
        return predicted_category, confidence
    except Exception as e:
        print(f"Error predicting waste class: {str(e)}")
        return None, 0.0
