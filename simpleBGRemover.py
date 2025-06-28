from PIL import Image, ImageFilter, ImageEnhance
import io

def remove_white_background(image_path):
    """
    Remove white/light backgrounds using only PIL
    """
    try:
        # Open image and convert to RGBA
        img = Image.open(image_path)
        img = img.convert("RGBA")
        
        # Get image data
        data = img.getdata()
        new_data = []
        
        # Process each pixel
        for item in data:
            # If pixel is white or very light, make it transparent
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                new_data.append((255, 255, 255, 0))  # Transparent
            else:
                new_data.append(item)  # Keep original
        
        # Apply new data
        img.putdata(new_data)
        return img
        
    except Exception as e:
        print(f"Error: {e}")
        # Return original if error
        original = Image.open(image_path)
        return original.convert('RGBA')

def create_cutout_effect(image_path):
    """
    Create a simple cutout effect
    """
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Create mask based on brightness
        grayscale = img.convert('L')
        
        # Create new image with transparency
        result = Image.new('RGBA', img.size, (0, 0, 0, 0))
        
        for x in range(img.width):
            for y in range(img.height):
                # Get grayscale value
                gray_val = grayscale.getpixel((x, y))
                
                # If pixel is dark enough, keep it
                if gray_val < 180:
                    result.putpixel((x, y), img.getpixel((x, y)))
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        original = Image.open(image_path)
        return original.convert('RGBA')

def smart_transparency(image_path):
    """
    Smart transparency based on color similarity
    """
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        
        # Get corner pixels to determine background color
        width, height = img.size
        corners = [
            img.getpixel((0, 0)),
            img.getpixel((width-1, 0)),
            img.getpixel((0, height-1)),
            img.getpixel((width-1, height-1))
        ]
        
        # Calculate average background color
        avg_r = sum(c[0] for c in corners) // 4
        avg_g = sum(c[1] for c in corners) // 4
        avg_b = sum(c[2] for c in corners) // 4
        
        # Process image
        data = img.getdata()
        new_data = []
        
        tolerance = 30  # Color tolerance
        
        for item in data:
            # Check if pixel is similar to background
            if (abs(item[0] - avg_r) < tolerance and 
                abs(item[1] - avg_g) < tolerance and 
                abs(item[2] - avg_b) < tolerance):
                new_data.append((255, 255, 255, 0))  # Transparent
            else:
                new_data.append(item)  # Keep original
        
        img.putdata(new_data)
        return img
        
    except Exception as e:
        print(f"Error: {e}")
        original = Image.open(image_path)
        return original.convert('RGBA')