#!/usr/bin/env python3
"""
Resize wallpaper images for TV launcher with blurred background.
For portrait/mismatched photos, creates a blurred background instead of cropping.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageFilter

def resize_with_blur_background(image_path, output_path, target_width=1920, target_height=1080, quality=90):
    """
    Resize image for TV display with blurred background for portrait photos.

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

    # Convert RGBA to RGB if needed
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (0, 0, 0))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background

    # Calculate aspect ratios
    img_aspect = img.width / img.height
    target_aspect = target_width / target_height

    # Decide strategy: blur background or crop
    aspect_diff = abs(img_aspect - target_aspect) / target_aspect

    if aspect_diff > 0.15:  # More than 15% difference - use blur background
        print(f"  Using blur background (aspect diff: {aspect_diff:.1%})")

        # Create blurred background
        # Scale image to cover target size
        if img_aspect > target_aspect:
            bg_width = target_width
            bg_height = int(bg_width / img_aspect)
        else:
            bg_height = target_height
            bg_width = int(bg_height * img_aspect)

        background = img.copy()
        background = background.resize((target_width, target_height), Image.Resampling.LANCZOS)
        background = background.filter(ImageFilter.GaussianBlur(radius=25))

        # Darken the background slightly
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        # Fit the original image within target size (contain, not cover)
        if img.width / target_width > img.height / target_height:
            # Width is the limiting factor
            new_width = target_width
            new_height = int(new_width / img_aspect)
        else:
            # Height is the limiting factor
            new_height = target_height
            new_width = int(new_height * img_aspect)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Center the image on the blurred background
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        background.paste(img, (x, y))

        final_img = background

    else:  # Similar aspect ratio - use smart crop
        print(f"  Using crop (aspect diff: {aspect_diff:.1%})")

        # Resize to cover the target size
        if img_aspect > target_aspect:
            new_height = target_height
            new_width = int(img_aspect * new_height)
        else:
            new_width = target_width
            new_height = int(new_width / img_aspect)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Center crop
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        final_img = img.crop((left, top, right, bottom))

    # Save as JPEG
    final_img.save(output_path, 'JPEG', quality=quality, optimize=True)

    # Check file size
    output_size = output_path.stat().st_size
    original_size_kb = image_path.stat().st_size / 1024
    output_size_kb = output_size / 1024
    print(f"  Output: {target_width}x{target_height}")
    print(f"  Size: {original_size_kb:.1f}KB -> {output_size_kb:.1f}KB")
    print()

def main():
    if len(sys.argv) < 3:
        print("Usage: resize_wallpapers_blur.py <input_folder> <output_folder>")
        print("Example: resize_wallpapers_blur.py themes/Family/originals themes/Family/wallpapers")
        sys.exit(1)

    input_folder = Path(sys.argv[1])
    output_folder = Path(sys.argv[2])

    if not input_folder.exists():
        print(f"Error: {input_folder} does not exist")
        sys.exit(1)

    # Create output folder
    output_folder.mkdir(parents=True, exist_ok=True)

    # Process all image files
    image_extensions = {'.jpg', '.jpeg', '.png'}
    images = [f for f in input_folder.iterdir()
              if f.suffix.lower() in image_extensions and f.name != 'screenshot.jpg']

    if not images:
        print(f"No images found in {input_folder}")
        sys.exit(1)

    print(f"Found {len(images)} images to resize")
    print(f"Output folder: {output_folder}\n")

    for img_path in sorted(images):
        output_path = output_folder / f"{img_path.stem}.jpg"
        try:
            resize_with_blur_background(img_path, output_path)
        except Exception as e:
            print(f"  Error: {e}\n")

    print(f"Done! Resized images saved to: {output_folder}")

if __name__ == '__main__':
    main()
