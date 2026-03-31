# Babel Universal Image Archive Generator

Inspired by Jorge Luis Borges' *"The Library of Babel"*, this program implements a **universal image archive** — a theoretical collection that contains **every possible image** at a given resolution and color depth.

No images are stored. They are computed on demand from their unique address.

## How It Works

1. Every image is a grid of pixels. Each pixel is one of `N` possible colors.
2. The entire pixel sequence maps to a unique large integer.
3. That integer, XOR-shuffled with a key and encoded in base-62, becomes the image's **address**.
4. Given an address → reconstruct the image. Given an image → compute its address.

Every photograph ever taken, every painting ever painted, every frame of every film — they all exist in this archive. So does every image that has never been seen.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Show archive statistics
python babel_image_archive.py stats

# Run the interactive demo
python babel_image_archive.py demo

# Retrieve an image by its address
python babel_image_archive.py browse <address>

# Find the address of an existing image
python babel_image_archive.py search photo.png

# Search and verify round-trip reconstruction
python babel_image_archive.py search photo.png --verify

# Generate random images from the archive
python babel_image_archive.py random --count 10
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--width` | Image width in pixels | 16 |
| `--height` | Image height in pixels | 16 |
| `--colors` | Colors per RGB channel | 8 |
| `--key` | Archive key for address shuffling | `babel` |
| `--scale` | Scale factor for output images | 16 |

## Examples

```bash
# Higher resolution archive (warning: addresses get very long)
python babel_image_archive.py --width 32 --height 32 stats

# Smaller palette for shorter addresses
python babel_image_archive.py --colors 4 demo

# Use a custom archive key (different key = different ordering)
python babel_image_archive.py --key "my_secret" demo
```
