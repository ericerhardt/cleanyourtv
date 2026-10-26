# Quick Start Guide

## TV Info
**IP Address:** `192.168.2.55`

## Most Common Commands

### Update Launcher Backgrounds
```bash
# 1. Put new photos in themes/Family/new-photos/
# 2. Resize them
python3 tools/resize_wallpapers_blur.py themes/Family/new-photos themes/Family/wallpapers

# 3. Push to TV
TV_HOST=192.168.2.55 tools/theme.sh themes/Family
```

### Take Screenshot
```bash
TV_HOST=192.168.2.55 tools/venv/bin/python tools/tv.py --screenshot screenshot.jpg
```

### Reset Theme
```bash
TV_HOST=192.168.2.55 tools/theme.sh --reset
```

## More Details
- **Family theme instructions:** `themes/Family/README.md`
- **Full memory of what we did:** `TV_SETUP_MEMORY.md`
