#!/usr/bin/env python3
"""
Update wines.json to add image_local paths pointing to optimized images.
This keeps the original 'image' URL as source of truth while providing a local fallback.
"""

import json
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent

# Define paths
wines_json_path = project_root / "src" / "feniks-data" / "wines.json"
images_dir = project_root / "src" / "feniks-data" / "images"


def main():
    """Main function to add image_local paths to wines.json."""
    # Load wines data
    try:
        with open(wines_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading wines.json: {e}")
        return 1

    wines = data.get("wines", [])
    
    if not wines:
        print("No wines found in wines.json")
        return 1

    print(f"Found {len(wines)} wines")
    print(f"Checking for local images in: {images_dir}\n")

    updated = 0
    missing = 0

    for i, wine in enumerate(wines, 1):
        form_number = wine.get("form_number", str(i))
        
        # Generate expected local image filename
        # The download script creates files as: wine_{form_number}_{original_filename}
        # But after optimization they're just JPG files
        wine_images = list(images_dir.glob(f"wine_{form_number}_*.jpg"))
        
        if wine_images:
            # Use the first matching JPG (there should only be one per wine)
            local_image = wine_images[0]
            relative_path = f"feniks-data/images/{local_image.name}"
            wine["image_local"] = relative_path
            print(f"✓ Wine {form_number}: {relative_path}")
            updated += 1
        else:
            print(f"✗ Wine {form_number}: No local image found (run optimize_images.py first)")
            missing += 1

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"Updated: {updated}")
    print(f"Missing: {missing}")
    print(f"{'='*60}\n")

    if updated > 0:
        # Save updated wines.json
        try:
            with open(wines_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Updated wines.json with image_local paths")
            print(f"\nThe HTML now uses image_local when available:")
            print(f"  if (wine.image_local) {{ use wine.image_local }}")
            print(f"  else {{ use wine.image (fallback to remote) }}")
            return 0
        except Exception as e:
            print(f"Error writing wines.json: {e}")
            return 1
    
    return 1 if missing > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
