import os
import shutil
import random
from pathlib import Path

def split_dataset(source_dir, train_dir, val_dir, val_ratio=0.2):
    # Create train and validation directories
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    
    # Get all class directories
    classes = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    
    for class_name in classes:
        # Create class directories in train and val
        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)
        
        # Get all images for this class
        class_dir = os.path.join(source_dir, class_name)
        images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Randomly split images
        random.shuffle(images)
        val_size = int(len(images) * val_ratio)
        val_images = images[:val_size]
        train_images = images[val_size:]
        
        # Copy images to respective directories
        for img in train_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(train_dir, class_name, img)
            shutil.copy2(src, dst)
            
        for img in val_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(val_dir, class_name, img)
            shutil.copy2(src, dst)
        
        print(f"Processed {class_name}: {len(train_images)} train, {len(val_images)} validation")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Define paths
    source_dir = "dataset"
    train_dir = "dataset/train"
    val_dir = "dataset/val"
    
    # Split the dataset
    split_dataset(source_dir, train_dir, val_dir)
    print("Dataset split complete!") 