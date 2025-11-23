#!/usr/bin/env python3
"""
Optimize wine images by resizing them to consistent square sizes with padding.
This script adds padding around narrow images instead of cropping.
"""

import os
import sys
from pathlib import Path
from PIL import Image

# Get the project root directory
project_root = Path(__file__).parent.parent

# Define paths
images_dir = project_root / "src" / "feniks-data" / "images"
output_dir = images_dir / "optimized"

# Configuration
TARGET_SIZE = 600  # Target square size in pixels
QUALITY = 85  # JPEG quality (1-100)
PADDING_COLOR = (255, 255, 255)  # White padding


def get_image_dimensions(image_path):
    """Get the dimensions of an image."""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"  Error reading image: {e}")
        return None


def resize_image_to_square(input_path, output_path, target_size=TARGET_SIZE):
    """Resize image to square with padding, preserving aspect ratio."""
    try:
        with Image.open(input_path) as img:
            # Convert RGBA/PNG to RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, PADDING_COLOR)
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            original_width, original_height = img.size
            
            # Calculate the scale to fit the image in the target size
            scale = min(target_size / original_width, target_size / original_height)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            
            # Resize the image
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create a new square image with white background
            square_img = Image.new('RGB', (target_size, target_size), PADDING_COLOR)
            
            # Calculate position to center the image
            x_offset = (target_size - new_width) // 2
            y_offset = (target_size - new_height) // 2
            
            # Paste the resized image onto the square canvas
            square_img.paste(img_resized, (x_offset, y_offset))
            
            # Save the optimized image
            square_img.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
            
            return True, new_width, new_height, original_width, original_height
    except Exception as e:
        print(f"  Error processing image: {e}")
        return False, None, None, None, None


def main():
    """Main function to optimize all wine images."""
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if images directory exists
    if not images_dir.exists():
        print(f"Error: Images directory not found at {images_dir}")
        print("Please run download_images.py first")
        return 1
    
    # Get all image files
    image_files = sorted([f for f in images_dir.glob("wine_*") if f.is_file()])
    
    if not image_files:
        print(f"No wine images found in {images_dir}")
        return 1
    
    print(f"Found {len(image_files)} wine images")
    print(f"Target size: {TARGET_SIZE}x{TARGET_SIZE} pixels")
    print(f"Output directory: {output_dir}\n")
    
    successful = 0
    failed = 0
    
    for image_file in image_files:
        filename = image_file.name
        output_path = output_dir / filename.replace('.png', '.jpg').replace('.PNG', '.jpg')
        
        print(f"Processing: {filename}")
        original_dims = get_image_dimensions(image_file)
        
        if not original_dims:
            print(f"  ✗ Failed to read image\n")
            failed += 1
            continue
        
        original_width, original_height = original_dims
        print(f"  Original size: {original_width}x{original_height}px")
        
        success, new_width, new_height, orig_w, orig_h = resize_image_to_square(
            image_file, output_path
        )
        
        if success:
            print(f"  Scaled to: {new_width}x{new_height}px")
            print(f"  ✓ Saved to: {output_path.name}")
            successful += 1
        else:
            print(f"  ✗ Failed to optimize\n")
            failed += 1
            continue
        
        print()
    
    print(f"\n{'='*60}")
    print(f"Optimization complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Optimized images saved to: {output_dir}")
    print(f"{'='*60}\n")
    
    if successful > 0:
        print("Next steps:")
        print(f"1. Review the optimized images in {output_dir}")
        print(f"2. Replace the original images:")
        print(f"   rm -rf {images_dir}/wine_*")
        print(f"   mv {output_dir}/* {images_dir}/")
        print(f"3. Remove the optimized directory:")
        print(f"   rmdir {output_dir}")
        print(f"4. Update wines.json to use local image paths")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
