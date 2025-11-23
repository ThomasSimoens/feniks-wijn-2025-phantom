# Feniks Wijn 2025 - Phantom Template

## About

This is a basic static website to list some of the offered wines for a temporary sale for the profits of a basketball club called Feniks Zwijnaarde.

It should only list the availble wines (which can be found at `src/feniks-data`) with some context.
No need for any "buy" or "shopping cart" functionality, because Feniks chose to have a Google Sheet form: `https://docs.google.com/forms/d/e/1FAIpQLSdSG1oNepLKLmEqgqf29_z72hex94BARXuJfIsfdfyPc67l3A/viewform`.

## Recommendations

1. Support three languages; "Nederlands" (default), "English" and "Francais"
2. Show the wines per category; "Bubbels", "Witte Wijn" and "Rode Wijn"
3. Wine images should all be shown consistently, all at the same size (as the original size and aspect ration can differ)
4. Even though we have individual URLs for all the wines, don't actually use them (because we want to actually guide them toward the Google Form where they can order to support the club)

## Local setup

The project is a static site. To preview locally, run a simple HTTP server from the project root. For example using Python 3:

```bash
cd src && python3 -m http.server 8000
```

Then open http://localhost:8000/ in your browser

## Image Management

### Setup Virtual Environment

To work with image scripts, first set up the virtual environment:

```bash
bash scripts/setup_venv.sh
```

This will create a `venv/` directory and install required dependencies (Pillow).

To activate the virtual environment in future sessions:

```bash
source venv/bin/activate
```

### Download Wine Images

Download all wine images from the remote URLs and save them locally:

```bash
python3 scripts/download_images.py
```

Images will be saved to `src/feniks-data/images/`

### Optimize Images

Resize all images to consistent square sizes (600x600px) with white padding:

```bash
python3 scripts/optimize_images.py
```

Optimized images will be saved to `src/feniks-data/images/optimized/`

Once satisfied with the results:

```bash
# Remove original downloaded images
rm -rf src/feniks-data/images/wine_*

# Move optimized images to main directory
mv src/feniks-data/images/optimized/* src/feniks-data/images/

# Remove the optimized subdirectory
rmdir src/feniks-data/images/optimized
```

Then update the image paths in `src/feniks-data/wines.json` to use local paths:

```json
"image": "feniks-data/images/wine_1_image.jpg"
```
