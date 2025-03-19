import os
import shutil
import random
from pathlib import Path

def organize_dataset(source_dir, train_dir, val_dir, val_ratio=0.2):
    # Create train and validation directories
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    
    # Get all class directories
    classes = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    
    # Map dataset classes to our model classes
    class_mapping = {
        'cardboard': 'paper',  # Map cardboard to paper
        'trash': 'organic'     # Map trash to organic
    }
    
    # Create e-waste directory (we'll add some images from trash category)
    os.makedirs(os.path.join(train_dir, 'e-waste'), exist_ok=True)
    os.makedirs(os.path.join(val_dir, 'e-waste'), exist_ok=True)
    
    for class_name in classes:
        # Determine target class name
        target_class = class_mapping.get(class_name, class_name)
        
        # Create class directories in train and val
        os.makedirs(os.path.join(train_dir, target_class), exist_ok=True)
        os.makedirs(os.path.join(val_dir, target_class), exist_ok=True)
        
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
            dst = os.path.join(train_dir, target_class, img)
            shutil.copy2(src, dst)
            
        for img in val_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(val_dir, target_class, img)
            shutil.copy2(src, dst)
        
        print(f"Processed {class_name} -> {target_class}: {len(train_images)} train, {len(val_images)} validation")
    
    # Add some e-waste images from trash category
    trash_dir = os.path.join(source_dir, 'trash')
    e_waste_images = [f for f in os.listdir(trash_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(e_waste_images)
    
    # Take 20% of trash images for e-waste
    e_waste_size = int(len(e_waste_images) * 0.2)
    e_waste_images = e_waste_images[:e_waste_size]
    
    # Split e-waste images between train and val
    e_waste_val_size = int(len(e_waste_images) * val_ratio)
    e_waste_val = e_waste_images[:e_waste_val_size]
    e_waste_train = e_waste_images[e_waste_val_size:]
    
    # Copy e-waste images
    for img in e_waste_train:
        src = os.path.join(trash_dir, img)
        dst = os.path.join(train_dir, 'e-waste', f'e_waste_{img}')
        shutil.copy2(src, dst)
    
    for img in e_waste_val:
        src = os.path.join(trash_dir, img)
        dst = os.path.join(val_dir, 'e-waste', f'e_waste_{img}')
        shutil.copy2(src, dst)
    
    print(f"Added e-waste category: {len(e_waste_train)} train, {len(e_waste_val)} validation")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Define paths
    source_dir = "dataset/Garbage classification/Garbage classification"
    train_dir = "dataset/train"
    val_dir = "dataset/val"
    
    # Organize the dataset
    organize_dataset(source_dir, train_dir, val_dir)
    print("Dataset organization complete!") 