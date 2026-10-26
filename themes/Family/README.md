# Family Theme Instructions

## TV Information
- **TV IP Address:** `192.168.2.55`
- **Theme Location:** `themes/Family/`
- **Launcher Package:** `com.gathin.tvhome`

## Current Setup
- **Wallpaper Count:** 7 family photos
- **Rotation:** Every 30 minutes
- **Order:** Shuffle (random)
- **Resolution:** 1920x1080 (Full HD)

## How to Add or Change Background Images

### Step 1: Add Your New Photos
Put your new photos (JPG, JPEG, or PNG) into a temporary folder, such as:
```bash
mkdir -p themes/Family/new-photos
# Copy your photos here
```

### Step 2: Resize the Photos
The resize script automatically handles both landscape and portrait photos:
- **Portrait photos** get a blurred background (no cropping)
- **Landscape photos** get smart-cropped to fit

Run the resize script:
```bash
python3 tools/resize_wallpapers_blur.py themes/Family/new-photos themes/Family/wallpapers
```

This will:
- Convert all images to 1920x1080 resolution
- Add blurred backgrounds for portrait photos
- Optimize file sizes (typically 200KB-700KB per image)
- Save processed images to `themes/Family/wallpapers/`

### Step 3: Push to TV
Push the updated theme to your TV:
```bash
TV_HOST=192.168.2.55 tools/theme.sh themes/Family
```

The launcher will restart automatically with the new photos.

### Step 4: Verify (Optional)
Take a screenshot to verify it looks good:
```bash
TV_HOST=192.168.2.55 tools/venv/bin/python tools/tv.py --screenshot themes/Family/test-screenshot.jpg
```

## To Remove Photos
Simply delete the unwanted image from `themes/Family/wallpapers/` and re-push:
```bash
rm themes/Family/wallpapers/unwanted-photo.jpg
TV_HOST=192.168.2.55 tools/theme.sh themes/Family
```

## To Change Rotation Settings
Edit `themes/Family/config.json`:
```json
{
  "wallpaper_rotation_minutes": 30,    // Change to 15, 60, etc.
  "wallpaper_order": "shuffle"         // Or "sequential"
}
```

Then push the updated config:
```bash
TV_HOST=192.168.2.55 tools/theme.sh themes/Family
```

## To Reset to Default Theme
```bash
TV_HOST=192.168.2.55 tools/theme.sh --reset
```

## Troubleshooting

### Python Dependencies Missing
If the resize script fails, install dependencies:
```bash
python3 -m venv tools/venv
tools/venv/bin/pip install -r tools/requirements.txt
```

### ADB Connection Issues
Make sure ADB is enabled on the TV:
1. Settings → Network → Check IP is still 192.168.2.55
2. Settings → Developer Options → USB Debugging: ON
3. Settings → Developer Options → Network Debugging: ON

### Check If Theme Is Active
```bash
TV_HOST=192.168.2.55 tools/venv/bin/python tools/tv.py --probe
```

## File Structure
```
themes/Family/
├── README.md              # This file
├── config.json            # Rotation settings
├── screenshot.jpg         # Theme preview
├── wallpapers/            # Active wallpapers (push these to TV)
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── ...
└── originals/             # Backup of original high-res photos
    └── ...
```
