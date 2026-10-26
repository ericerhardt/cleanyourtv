# TV Setup Memory

## TV Configuration
- **Model:** (Add your TV model here)
- **IP Address:** `192.168.2.55`
- **Android Version:** (Add version here)
- **Launcher:** Custom launcher from this repo (`com.gathin.tvhome`)
- **Theme:** Family (rotating family photos)

## What Was Done

### Session: October 26, 2024

#### Problem
- Uploaded family photos as launcher backgrounds
- Images were incorrectly sized/cropped
- Portrait photos were being severely cropped, cutting off people's heads/feet

#### Solution
1. **Created resize script with blur background feature**
   - Location: `tools/resize_wallpapers_blur.py`
   - Handles portrait photos by adding darkened blurred background
   - Handles landscape photos with smart center-crop
   - Outputs at 1920x1080 (Full HD)

2. **Processed 7 family photos**
   - Original photos: `Photos-1-001.zip` → extracted to `themes/Family/originals/`
   - Resized photos: `themes/Family/wallpapers/`
   - Portrait photos (3072x4080) now show full image with blur background
   - Landscape photos properly cropped to 16:9

3. **Theme configuration**
   - File: `themes/Family/config.json`
   - Rotation: 30 minutes
   - Order: Shuffle

4. **Successfully pushed to TV**
   - Command: `TV_HOST=192.168.2.55 tools/theme.sh themes/Family`
   - Verified with screenshot
   - Result: Much better display, no harsh cropping

## Quick Reference Commands

### Push Family Theme to TV
```bash
TV_HOST=192.168.2.55 tools/theme.sh themes/Family
```

### Take Screenshot from TV
```bash
TV_HOST=192.168.2.55 tools/venv/bin/python tools/tv.py --screenshot output.jpg
```

### Resize New Photos
```bash
python3 tools/resize_wallpapers_blur.py <source_folder> themes/Family/wallpapers
```

### Reset to Default Theme
```bash
TV_HOST=192.168.2.55 tools/theme.sh --reset
```

### Check TV Connection
```bash
TV_HOST=192.168.2.55 tools/venv/bin/python tools/tv.py --probe
```

## Scripts Created

### tools/resize_wallpapers_blur.py
Advanced wallpaper resizer that:
- Detects aspect ratio differences
- Uses blurred background for portrait photos (>15% aspect difference)
- Uses smart crop for landscape photos (<15% aspect difference)
- Darkens background for better launcher text visibility
- Optimizes file size while maintaining quality

Usage:
```bash
python3 tools/resize_wallpapers_blur.py <input_folder> <output_folder>
```

### tools/resize_wallpapers.py
Simple wallpaper resizer (created but not used):
- Always uses center-crop approach
- No blur background
- Use `resize_wallpapers_blur.py` instead for better results

## File Locations

### Theme Files
- **Theme folder:** `themes/Family/`
- **Config:** `themes/Family/config.json`
- **Active wallpapers:** `themes/Family/wallpapers/` (7 JPGs, ~200-700KB each)
- **Original photos:** `themes/Family/originals/` (backup of high-res originals)
- **Instructions:** `themes/Family/README.md`

### Source Archive
- **Original photos zip:** `Photos-1-001.zip` (29MB, 7 photos)

## Python Environment

The scripts require Python 3 with Pillow library:
```bash
# Virtual environment (if needed)
python3 -m venv tools/venv
tools/venv/bin/pip install -r tools/requirements.txt

# Or use system Python (Pillow 12.2.0 already installed)
python3 -c "import PIL; print(PIL.__version__)"
```

## For Future Sessions

When adding/changing launcher background images:
1. Read `themes/Family/README.md` for detailed instructions
2. Use `tools/resize_wallpapers_blur.py` to process new photos
3. Push with `TV_HOST=192.168.2.55 tools/theme.sh themes/Family`
4. TV IP address is `192.168.2.55`

## Notes
- Always keep backups of original high-resolution photos
- The blur background approach preserves the full photo without harsh cropping
- Theme rotation is configured in `config.json`
- All changes are reversible with `tools/theme.sh --reset`
