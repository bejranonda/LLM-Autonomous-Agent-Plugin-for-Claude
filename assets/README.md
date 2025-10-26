# Assets Directory

This directory contains visual assets for the Autonomous Claude Agent Plugin marketplace listing.

## Required Assets

### Icon (icon.png) ✅
- **Status**: **PRESENT** - Logo integrated
- **Dimensions**: 275x275 pixels (275 x 275 PNG)
- **Format**: PNG with RGB color
- **Size**: 59KB
- **Source**: Logo LLM-275x275.png
- **Content**: LLM autonomous agent logo

### Screenshots

Place screenshots in the `screenshots/` subdirectory:

#### 1. autonomous-analysis.png
- **Description**: Shows the `/analyze:project` command in action
- **Content**: Terminal output showing autonomous code analysis with skill auto-selection
- **Recommended size**: 1920x1080 or 1280x720

#### 2. quality-control.png
- **Description**: Shows the `/analyze:quality` command with auto-fix loop
- **Content**: Terminal output showing quality assessment, failed checks, and automatic corrections
- **Recommended size**: 1920x1080 or 1280x720

#### 3. pattern-learning.png
- **Description**: Shows pattern learning system in action
- **Content**: Terminal or visualization showing pattern storage and retrieval
- **Recommended size**: 1920x1080 or 1280x720

## How to Add Assets

### Option 1: Create Icon with Design Tools
Use tools like:
- Figma (https://figma.com)
- Canva (https://canva.com)
- GIMP (free, https://gimp.org)
- Photoshop

### Option 2: Generate Icon with AI
Use AI image generators:
- DALL-E (https://openai.com/dall-e)
- Midjourney (https://midjourney.com)
- Stable Diffusion

**Prompt example**:
```
"A minimal, modern icon representing an autonomous AI agent with learning capabilities.
Circuit brain pattern in blue and purple gradients. Clean, professional design suitable
for a developer tool. 256x256 pixels, PNG format, transparent background."
```

### Option 3: Use Free Icon Resources
- Font Awesome (https://fontawesome.com)
- Material Icons (https://material.io/icons)
- Feather Icons (https://feathericons.com)

### Creating Screenshots

1. Install the plugin in Claude Code
2. Navigate to a test project
3. Run each command:
   ```bash
   /analyze:project
   /analyze:quality
   /learn:init
   ```
4. Capture terminal output with screenshot tool:
   - **Windows**: Win + Shift + S
   - **Mac**: Cmd + Shift + 4
   - **Linux**: gnome-screenshot or spectacle

5. Save with appropriate filename in `screenshots/` directory

## Temporary Placeholders

Until real assets are created, the plugin will work without them. The marketplace listing will just display text-only information.

To temporarily disable asset references in plugin.json, remove or comment out these lines:
```json
"icon": "assets/icon.png",
"screenshots": [
  "assets/screenshots/autonomous-analysis.png",
  "assets/screenshots/quality-control.png",
  "assets/screenshots/pattern-learning.png"
]
```

## Asset Checklist

- [x] Create or generate icon.png (275x275) ✅ **COMPLETE**
- [ ] Take screenshot: autonomous-analysis.png
- [ ] Take screenshot: quality-control.png
- [ ] Take screenshot: pattern-learning.png
- [x] Verify icon is optimized (59KB < 500KB) ✅ **COMPLETE**
- [x] Test plugin.json references icon correctly ✅ **COMPLETE**

## Image Optimization

Before committing, optimize images to reduce repository size:

### Using ImageOptim (Mac)
```bash
brew install imageoptim
imageoptim assets/**/*.png
```

### Using pngquant (Cross-platform)
```bash
# Install
brew install pngquant  # Mac
apt install pngquant   # Linux
choco install pngquant # Windows

# Optimize
pngquant assets/**/*.png --ext .png --force
```

### Using online tools
- TinyPNG: https://tinypng.com
- Squoosh: https://squoosh.app

## Notes

- All assets are optional but highly recommended for marketplace visibility
- High-quality screenshots significantly improve plugin adoption
- Keep total assets size under 5MB for faster downloads
- Use descriptive alt text in marketplace submission
