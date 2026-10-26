#!/usr/bin/env python3
"""
Resize wallpaper images for TV launcher backgrounds.
Optimizes images to 1920x1080, maintaining aspect ratio with center crop.
"""

import os
import sys
from pathlib import Path
from PIL import Image

def resize_for_tv(image_path, output_path, target_width=1920, target_height=1080, quality=90):
    """
    Resize and optimize an image for TV display.

    Args:
        image_path: Input image file
        output_path: Output image file
        target_width: Target width (default 1920 for Full HD)
        target_height: Target height (default 1080 for Full HD)
        quality: JPEG quality (default 90)
    """
    print(f"Processing: {image_path.name}")

    # Open image
    img = Image.open(image_path)
    original_size = img.size
    print(f"  Original: {original_size[0]}x{original_size[1]}")

    # Convert RGBA to RGB if needed (for PNG with transparency)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (0, 0, 0))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background

    # Calculate aspect ratios
    img_aspect = img.width / img.height
    target_aspect = target_width / target_height

    # Resize to cover the target size (crop to fit)
    if img_aspect > target_aspect:
        # Image is wider - fit to height and crop width
        new_height = target_height
        new_width = int(img_aspect * new_height)
    else:
        # Image is taller - fit to width and crop height
        new_width = target_width
        new_height = int(new_width / img_aspect)

    # Resize with high-quality resampling
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Center crop to exact target size
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    img = img.crop((left, top, right, bottom))

    # Save as JPEG with optimization
    img.save(output_path, 'JPEG', quality=quality, optimize=True)

    # Check file size
    output_size = output_path.stat().st_size
    original_size_kb = image_path.stat().st_size / 1024
    output_size_kb = output_size / 1024
    print(f"  Output: {target_width}x{target_height}")
    print(f"  Size: {original_size_kb:.1f}KB -> {output_size_kb:.1f}KB")
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: resize_wallpapers.py <theme_folder>")
        print("Example: resize_wallpapers.py themes/Family")
        sys.exit(1)

    theme_folder = Path(sys.argv[1])

    if not theme_folder.exists():
        print(f"Error: {theme_folder} does not exist")
        sys.exit(1)

    # Create resized folder
    resized_folder = theme_folder / "resized"
    resized_folder.mkdir(exist_ok=True)

    # Process all image files
    image_extensions = {'.jpg', '.jpeg', '.png'}
    images = [f for f in theme_folder.iterdir()
              if f.suffix.lower() in image_extensions and f.name != 'screenshot.jpg']

    if not images:
        print(f"No images found in {theme_folder}")
        sys.exit(1)

    print(f"Found {len(images)} images to resize")
    print(f"Output folder: {resized_folder}\n")

    for img_path in sorted(images):
        output_path = resized_folder / f"{img_path.stem}.jpg"
        try:
            resize_for_tv(img_path, output_path)
        except Exception as e:
            print(f"  Error: {e}\n")

    print(f"Done! Resized images saved to: {resized_folder}")
    print(f"\nTo use these images:")
    print(f"1. Replace the original images with the resized versions")
    print(f"2. Use tools/tv.py to push the theme to your TV")

if __name__ == '__main__':
    main()
