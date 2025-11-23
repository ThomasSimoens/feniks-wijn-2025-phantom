#!/usr/bin/env python3
"""
Download wine images from feniks-data/wines.json and save them locally.
This script downloads images and prepares them for optimization.
"""

import json
import os
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

# Get the project root directory
project_root = Path(__file__).parent.parent

# Define paths
wines_json_path = project_root / "src" / "feniks-data" / "wines.json"
images_dir = project_root / "src" / "feniks-data" / "images"

# Ensure images directory exists
images_dir.mkdir(parents=True, exist_ok=True)


def get_filename_from_url(url):
    """Extract filename from URL, handling query parameters."""
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    return filename if filename else "image.jpg"


def download_image(url, save_path, wine_title):
    """Download an image from URL to save_path."""
    try:
        print(f"Downloading: {wine_title}")
        print(f"  URL: {url}")
        
        # Set a user agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(save_path, 'wb') as out_file:
                out_file.write(response.read())
        
        print(f"  ✓ Saved to: {save_path.name}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Main function to download all wine images."""
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
    print(f"Downloading images to: {images_dir}\n")

    successful = 0
    failed = 0

    for i, wine in enumerate(wines, 1):
        url = wine.get("image")
        title = wine.get("title", f"Wine {i}")
        
        if not url:
            print(f"Skipping: {title} (no image URL)")
            continue

        # Generate filename from form_number or index
        form_number = wine.get("form_number", str(i))
        filename = f"wine_{form_number}_{get_filename_from_url(url)}"
        save_path = images_dir / filename

        if save_path.exists():
            print(f"Already exists: {title}")
            print(f"  Skipped: {filename}\n")
            continue

        if download_image(url, save_path, title):
            successful += 1
        else:
            failed += 1
        
        print()

    print(f"\n{'='*60}")
    print(f"Download complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Images saved to: {images_dir}")
    print(f"{'='*60}\n")

    # Print a note about updating the JSON
    if successful > 0:
        print("Next steps:")
        print(f"Don't forget to update the src image paths to point to local images")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
