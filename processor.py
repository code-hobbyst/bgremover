import cv2
import numpy as np
from PIL import Image
import io

def remove_background_simple(image_path):
    """
    Simple background removal using OpenCV
    This is a basic implementation for demonstration
    """
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image")
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to grayscale for processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply GaussianBlur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply threshold to create a binary mask
        _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create mask
        mask = np.zeros(gray.shape, dtype=np.uint8)
        
        if contours:
            # Find the largest contour (assuming it's the main subject)
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.fillPoly(mask, [largest_contour], 255)
        
        # Convert to RGBA
        img_rgba = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2RGBA)
        
        # Apply mask to alpha channel
        img_rgba[:, :, 3] = mask
        
        # Convert to PIL Image
        pil_image = Image.fromarray(img_rgba)
        
        return pil_image
        
    except Exception as e:
        print(f"Error in background removal: {e}")
        # Return original image as RGBA if processing fails
        original = Image.open(image_path)
        if original.mode != 'RGBA':
            original = original.convert('RGBA')
        return original

def create_transparent_background(image_path):
    """
    Alternative simple method - makes white/light backgrounds transparent
    """
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        
        data = img.getdata()
        new_data = []
        
        for item in data:
            # Make white and light colors transparent
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                new_data.append((255, 255, 255, 0))  # Transparent
            else:
                new_data.append(item)
        
        img.putdata(new_data)
        return img
        
    except Exception as e:
        print(f"Error in transparency processing: {e}")
        # Return original image if processing fails
        original = Image.open(image_path)
        if original.mode != 'RGBA':
            original = original.convert('RGBA')
        return original