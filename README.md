# Babel Universal Image Archive Generator

Inspired by Jorge Luis Borges' *"The Library of Babel"*, this is a **commercial-grade web application** implementing a universal image archive — a theoretical collection containing **every possible image** at a given resolution and color depth.

No images are stored. They are computed on demand from their unique address.

## How It Works

1. Every image is a grid of pixels. Each pixel is one of `N` possible colors.
2. The entire pixel sequence maps to a unique large integer.
3. That integer is encrypted (XOR or Feistel cipher) and encoded in base-62 as the image's **address**.
4. Given an address, reconstruct the image. Given an image, compute its address. Nothing is stored.

At default settings (16x16 resolution, 512 colors), the archive contains **~3.7 x 10^693 images** — a number that dwarfs the atoms in the observable universe.

## Features

- **Web Application** — Full Flask web app with dark-themed commercial UI
- **Browse** — Enter any base-62 address to retrieve its image
- **Search** — Upload any image to find its exact address in the archive
- **Random** — Generate random images from the infinite archive
- **Gallery** — Navigate rooms, walls, and shelves (Library of Babel style)
- **Explore** — View neighboring addresses and navigate spatially
- **REST API** — Full JSON API with CORS support
- **CLI Tool** — Original command-line interface still included
- **Color Modes** — RGB, Grayscale, Black & White
- **Shuffle Modes** — XOR cipher (fast) or Feistel FPE (cryptographic permutation)
- **Immutable Caching** — Deterministic images with aggressive cache headers
- **Responsive** — Mobile-friendly
- **Production Ready** — WSGI entry point, configurable via environment variables

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start — Web Application

```bash
# Development server
python app.py

# Production (gunicorn)
gunicorn wsgi:application -w 4 -b 0.0.0.0:8000
```

Then open http://localhost:5000 (dev) or http://localhost:8000 (prod).

## CLI Usage

```bash
python babel_image_archive.py stats          # Show archive statistics
python babel_image_archive.py demo           # Run interactive demo
python babel_image_archive.py browse <addr>  # Retrieve image by address
python babel_image_archive.py search img.png # Find address of an image
python babel_image_archive.py random -n 10   # Generate random images
```

## REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/browse/<address>` | Retrieve image by address (JSON with base64) |
| POST | `/api/v1/search` | Upload image to find its address |
| GET | `/api/v1/random?count=N` | Generate N random images |
| GET | `/api/v1/stats` | Archive configuration and statistics |
| GET | `/api/v1/gallery/<room>/<wall>/<shelf>` | Gallery shelf contents |
| GET | `/api/v1/explore/<address>` | Neighboring addresses |
| GET | `/image/<address>.png?scale=N` | Raw PNG image (for `<img>` tags) |

## Configuration

Set via environment variables or `config.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `BABEL_WIDTH` | Image width in pixels | 16 |
| `BABEL_HEIGHT` | Image height in pixels | 16 |
| `BABEL_COLORS` | Colors per RGB channel | 8 |
| `BABEL_KEY` | Archive encryption key | `babel` |
| `BABEL_COLOR_MODE` | `rgb`, `grayscale`, or `bw` |
| `BABEL_SHUFFLE_MODE` | `xor` or `feistel` |
| `BABEL_SCALE` | Default display scale factor | 16 |
| `SECRET_KEY` | Flask secret key | (set in production) |

## Project Structure

```
babel_engine.py          # Core engine — reversible image<->address mapping
app.py                   # Flask web application with all routes + API
config.py                # Application configuration (dev/prod)
wsgi.py                  # WSGI entry point for production deployment
babel_image_archive.py   # Standalone CLI tool
requirements.txt         # Python dependencies
templates/
  base.html              # Base layout (dark theme, navigation)
  index.html             # Landing page with hero section
  browse.html            # Browse by address
  search.html            # Upload & search
  random.html            # Random image generation
  gallery.html           # Room/wall/shelf navigation
  explore.html           # Spatial exploration
  stats.html             # Statistics & API docs
  errors/                # 404, 500 error pages
static/
  css/style.css          # Commercial dark theme stylesheet
  js/app.js              # Client-side interactions
```

---

## Open Bitcoin research challenge: MAPAE

This repository also hosts the **Million-Address Perpetual Adversarial Exposure Experiment**, a lawful public challenge involving one million committed Bitcoin `bc1q...` addresses and an initial public address cohort.

- [MAPAE research record and challenge rules](MAPAE/README.md)
- [Tier Ω flagship public addresses](MAPAE/tier-omega-100.txt)
- [Tier A public addresses 1–100](MAPAE/tier-a-public/tier-a-0001-0100.txt)
- [Tier A public addresses 101–200](MAPAE/tier-a-public/tier-a-0101-0200.txt)
- Canonical one-million-address SHA-256: `5bb9320bc93f07e3129cb6ef5aee4da2c245e0ca11279d4963244bead79a90df`

The MAPAE publication contains public Bitcoin addresses only. It contains no private keys, seeds, mnemonics, WIFs, or recovery secrets.
