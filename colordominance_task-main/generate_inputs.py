import os
import json
import random
import math
from PIL import Image, ImageDraw

# Define color palette with RGB values and names
COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42),
    "gray": (128, 128, 128),
    "black": (0, 0, 0),
    "white": (255, 255, 255)
}

def draw_random_shape(draw, color, image_size):
    """Draw a random shape (rectangle, circle, or polygon) with the given color."""
    # Random position and size
    size = random.randint(30, min(120, image_size // 3))
    x = random.randint(0, image_size - size)
    y = random.randint(0, image_size - size)
    
    shape_type = random.choice(["rectangle", "circle", "polygon"])
    
    if shape_type == "rectangle":
        draw.rectangle([x, y, x + size, y + size], fill=color)
    elif shape_type == "circle":
        draw.ellipse([x, y, x + size, y + size], fill=color)
    elif shape_type == "polygon":
        # Create a random triangle
        points = [
            (x + size // 2, y),
            (x, y + size),
            (x + size, y + size)
        ]
        draw.polygon(points, fill=color)

def calculate_color_areas(image):
    """Calculate the area covered by each color in the image."""
    color_areas = {}
    width, height = image.size
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            # Skip white background
            if pixel == (255, 255, 255):
                continue
                
            # Find closest color name
            closest_color = None
            min_distance = float('inf')
            
            for color_name, color_rgb in COLORS.items():
                distance = sum((a - b) ** 2 for a, b in zip(pixel, color_rgb))
                if distance < min_distance:
                    min_distance = distance
                    closest_color = color_name
            
            if closest_color:
                color_areas[closest_color] = color_areas.get(closest_color, 0) + 1
    
    return color_areas

def generate_dataset(output_dir, num_images=15, image_size=512, 
                    min_regions=3, max_regions=8):
    """Generate a dataset of images with dominant colors."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    input_dir = os.path.join(output_dir, "input")
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    gt = {}

    for i in range(1, num_images + 1):
        # Create white background
        img = Image.new("RGB", (image_size, image_size), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Select colors for this image
        num_regions = random.randint(min_regions, max_regions)
        available_colors = list(COLORS.keys())
        selected_colors = random.sample(available_colors, min(num_regions, len(available_colors)))
        
        # Ensure we have at least 2 colors
        if len(selected_colors) < 2:
            selected_colors.extend(random.sample([c for c in available_colors if c not in selected_colors], 2 - len(selected_colors)))
        
        # Draw regions with varying sizes to create dominance
        for j, color_name in enumerate(selected_colors):
            color_rgb = COLORS[color_name]
            # Make one color dominant by drawing more/larger regions
            if j == 0:  # First color gets more regions
                num_shapes = random.randint(3, 6)
            else:
                num_shapes = random.randint(1, 3)
            
            for _ in range(num_shapes):
                draw_random_shape(draw, color_rgb, image_size)
        
        # Calculate actual dominant color
        color_areas = calculate_color_areas(img)
        if color_areas:
            dominant_color = max(color_areas, key=color_areas.get)
        else:
            dominant_color = selected_colors[0]  # Fallback
        
        filename = "image_{}.png".format(i)
        img.save(os.path.join(input_dir, filename))
        gt[filename] = dominant_color

    # Write ground truth colors JSON
    with open(os.path.join(output_dir, "ground_truth_colors.json"), "w") as f:
        json.dump(gt, f, indent=2)

    # Write targets.json for some agents
    targets_path = os.path.join(output_dir, "input", "targets.json")
    with open(targets_path, "w") as f:
        json.dump(gt, f, indent=2)

    print("Generated {} images with dominant colors:".format(num_images))
    for filename, color in gt.items():
        print("  {}: {}".format(filename, color))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=os.path.dirname(__file__))
    parser.add_argument("--n", type=int, default=15, help="number of images")
    parser.add_argument("--min_regions", type=int, default=3)
    parser.add_argument("--max_regions", type=int, default=8)
    args = parser.parse_args()
    generate_dataset(args.out, args.n, min_regions=args.min_regions, max_regions=args.max_regions)
