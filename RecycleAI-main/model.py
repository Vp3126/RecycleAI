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

class WasteClassifier:
    """
    A classifier that uses image features for waste classification
    """
    def __init__(self):
        self.categories = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._create_model()
        # Load trained weights
        try:
            self.load_weights('waste_model.pth')
        except:
            try:
                self.load_weights('../waste_model.pth')
            except Exception as e:
                print(f"Error loading model weights: {str(e)}")
                raise
    
    def _create_model(self):
        # Load pre-trained ResNet50
        model = models.resnet50(pretrained=True)
        
        # Modify the final layer for our 6 classes
        num_features = model.fc.in_features
        model.fc = nn.Linear(num_features, len(self.categories))
        
        return model.to(self.device)
    
    def load_weights(self, weights_path):
        """Load trained weights"""
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.model.eval()
    
    def predict(self, image_array):
        """Predict using the deep learning model"""
        # Convert numpy array to tensor
        if isinstance(image_array, np.ndarray):
            image_array = torch.from_numpy(image_array).float()
        
        # Add batch dimension if not present
        if len(image_array.shape) == 3:
            image_array = image_array.unsqueeze(0)
        
        # Move to device
        image_array = image_array.to(self.device)
        
        # Get prediction
        with torch.no_grad():
            outputs = self.model(image_array)
            probabilities = torch.softmax(outputs, dim=1)
            probabilities = probabilities.cpu().numpy()[0]
        
        return probabilities

def load_model():
    try:
        # Try loading from current directory first
        model_path = "waste_model.pth"
        if not os.path.exists(model_path):
            # Try loading from parent directory
            model_path = "../waste_model.pth"
        
        if not os.path.exists(model_path):
            print(f"Model file not found at {model_path}")
            return None
            
        print(f"Loading model from: {model_path}")
        
        # Load the model with pretrained weights for better feature extraction
        model = models.resnet50(pretrained=True)
        num_classes = len(WASTE_CATEGORIES)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        
        # Load state dict
        state_dict = torch.load(model_path, map_location=torch.device('cpu'))
        print("Model state dict keys:", state_dict.keys())
        
        # Load weights
        model.load_state_dict(state_dict)
        
        # Set model to evaluation mode
        model.eval()
        
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None

def preprocess_image(image):
    try:
        # Convert PIL Image to RGB if it's not
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Define the preprocessing transforms with data augmentation
        preprocess = transforms.Compose([
            transforms.Resize((256, 256)),  # Resize to larger size first
            transforms.CenterCrop(224),     # Center crop to final size
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
            return None, 0.0
            
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            # Get top 3 predictions for debugging
            top3_prob, top3_indices = torch.topk(probabilities, 3)
            
            # Print top 3 predictions for debugging
            print("\nTop 3 predictions:")
            for i in range(3):
                idx = top3_indices[0][i].item()
                prob = top3_prob[0][i].item() * 100
                print(f"{WASTE_CATEGORIES[idx]}: {prob:.2f}%")
            
            # Get the highest probability prediction
            confidence, predicted = torch.max(probabilities, 1)
            confidence = confidence.item() * 100
            predicted_category = WASTE_CATEGORIES[predicted.item()]
            
            # Special handling for plastic items
            plastic_idx = WASTE_CATEGORIES.index('plastic')
            paper_idx = WASTE_CATEGORIES.index('paper')
            
            # If the prediction is paper and plastic is in top 2 with decent confidence
            if predicted_category == 'paper' and confidence < 70:  # Increased threshold
                # Check if plastic is in top 2 predictions
                for i in range(2):
                    if top3_indices[0][i].item() == plastic_idx:
                        plastic_prob = top3_prob[0][i].item() * 100
                        if plastic_prob > 35:  # Increased threshold for plastic confidence
                            predicted_category = 'plastic'
                            confidence = plastic_prob
                            break
            
            # If confidence is too low, try to use the second best prediction
            elif confidence < 45 and top3_prob[0][1].item() * 100 > 35:  # Adjusted thresholds
                # If the second best prediction is glass or plastic, use it
                second_best_idx = top3_indices[0][1].item()
                second_best_category = WASTE_CATEGORIES[second_best_idx]
                if second_best_category in ['glass', 'plastic']:
                    predicted_category = second_best_category
                    confidence = top3_prob[0][1].item() * 100
            
            # Additional check for plastic items
            if predicted_category == 'paper' and confidence < 80:  # Very high threshold for paper
                plastic_prob = probabilities[0][plastic_idx].item() * 100
                if plastic_prob > 40:  # If plastic has significant confidence
                    predicted_category = 'plastic'
                    confidence = plastic_prob
            
            return predicted_category, confidence
    except Exception as e:
        print(f"Error predicting waste class: {str(e)}")
        return None, 0.0
