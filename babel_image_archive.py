"""
Babel Universal Image Archive Generator

Inspired by Jorge Luis Borges' "The Library of Babel", this program implements
a universal image archive — a theoretical collection of every possible image
at a given resolution and color depth.

Core concept: Every image is a sequence of pixels. Each pixel sequence maps to
a unique integer (its "address"). Given an address, we can reconstruct the exact
image. Given an image, we can compute its exact address. No images are stored —
they are computed on demand.

Features:
  - Generate any image from its unique address (Browse)
  - Find the exact address of any input image (Search)
  - Generate random images from the archive (Random)
  - Configurable resolution and color depth
  - XOR cipher with key for shuffled archive ordering
"""

import argparse
import hashlib
import math
import os
import random
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_WIDTH = 16
DEFAULT_HEIGHT = 16
DEFAULT_COLORS = 8  # colors per channel (RGB), total palette = colors^3
DEFAULT_KEY = "babel"

BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


# =============================================================================
# Address Encoding / Decoding (bijective base-62)
# =============================================================================

def int_to_base62(n):
    """Convert a non-negative integer to a base-62 string."""
    if n == 0:
        return BASE62_CHARS[0]
    digits = []
    while n > 0:
        digits.append(BASE62_CHARS[n % 62])
        n //= 62
    return "".join(reversed(digits))


def base62_to_int(s):
    """Convert a base-62 string back to a non-negative integer."""
    n = 0
    for ch in s:
        idx = BASE62_CHARS.index(ch)
        if idx < 0:
            raise ValueError(f"Invalid base-62 character: {ch}")
        n = n * 62 + idx
    return n


# =============================================================================
# XOR Cipher for Address Shuffling
# =============================================================================

def derive_keystream(key, length):
    """Derive a deterministic keystream from a string key using SHA-256 chaining."""
    keystream = bytearray()
    counter = 0
    while len(keystream) < length:
        h = hashlib.sha256(f"{key}:{counter}".encode()).digest()
        keystream.extend(h)
        counter += 1
    return bytes(keystream[:length])


def xor_shuffle(data_int, key, byte_length):
    """XOR an integer with a key-derived stream to shuffle the address space."""
    data_bytes = data_int.to_bytes(byte_length, byteorder="big")
    keystream = derive_keystream(key, byte_length)
    xored = bytes(a ^ b for a, b in zip(data_bytes, keystream))
    return int.from_bytes(xored, byteorder="big")


# =============================================================================
# Core Archive Engine
# =============================================================================

class BabelImageArchive:
    """
    The Universal Image Archive.

    Every possible image of the configured resolution and color depth exists
    within this archive and can be retrieved by its unique address.
    """

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                 colors_per_channel=DEFAULT_COLORS, key=DEFAULT_KEY):
        self.width = width
        self.height = height
        self.colors_per_channel = colors_per_channel
        self.palette_size = colors_per_channel ** 3  # total distinct colors
        self.total_pixels = width * height
        self.key = key

        # Total number of possible images
        self.total_images = self.palette_size ** self.total_pixels

        # Byte length needed to represent the largest image index
        self.byte_length = math.ceil(self.total_images.bit_length() / 8)

        # Quantization step for mapping palette index -> 0-255 RGB
        self.quant_step = max(1, 255 // (colors_per_channel - 1))

    def _index_to_color(self, idx):
        """Convert a palette index to an (R, G, B) tuple."""
        cpc = self.colors_per_channel
        b = idx % cpc
        g = (idx // cpc) % cpc
        r = (idx // (cpc * cpc)) % cpc
        return (
            min(r * self.quant_step, 255),
            min(g * self.quant_step, 255),
            min(b * self.quant_step, 255),
        )

    def _color_to_index(self, r, g, b):
        """Convert an (R, G, B) tuple to the nearest palette index."""
        cpc = self.colors_per_channel
        ri = min(round(r / self.quant_step), cpc - 1)
        gi = min(round(g / self.quant_step), cpc - 1)
        bi = min(round(b / self.quant_step), cpc - 1)
        return ri * cpc * cpc + gi * cpc + bi

    def _int_to_pixels(self, n):
        """Convert an integer to a list of palette indices (pixel sequence)."""
        pixels = []
        for _ in range(self.total_pixels):
            pixels.append(n % self.palette_size)
            n //= self.palette_size
        return list(reversed(pixels))

    def _pixels_to_int(self, pixels):
        """Convert a list of palette indices back to an integer."""
        n = 0
        for p in pixels:
            n = n * self.palette_size + p
        return n

    def address_to_image(self, address):
        """
        Retrieve an image from the archive by its address.

        Args:
            address: A base-62 encoded string representing the image location.

        Returns:
            A PIL Image object.
        """
        raw_int = base62_to_int(address)
        if raw_int >= self.total_images:
            raise ValueError(
                f"Address out of range. Max address: {int_to_base62(self.total_images - 1)}"
            )
        # Unshuffle via XOR
        image_int = xor_shuffle(raw_int, self.key, self.byte_length)
        image_int %= self.total_images  # ensure within bounds after XOR

        pixels = self._int_to_pixels(image_int)

        img = Image.new("RGB", (self.width, self.height))
        img_pixels = img.load()
        for i, p in enumerate(pixels):
            x = i % self.width
            y = i // self.width
            img_pixels[x, y] = self._index_to_color(p)

        return img

    def image_to_address(self, img):
        """
        Find the address of an image in the archive.

        The image is quantized to the archive's color depth before lookup.

        Args:
            img: A PIL Image object.

        Returns:
            A base-62 encoded address string.
        """
        img = img.convert("RGB").resize((self.width, self.height), Image.LANCZOS)

        pixels = []
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = img.getpixel((x, y))
                pixels.append(self._color_to_index(r, g, b))

        image_int = self._pixels_to_int(pixels)
        # Shuffle via XOR (same operation reverses itself)
        raw_int = xor_shuffle(image_int, self.key, self.byte_length)
        raw_int %= self.total_images

        return int_to_base62(raw_int)

    def random_address(self):
        """Generate a random address within the archive."""
        n = random.randint(0, self.total_images - 1)
        return int_to_base62(n)

    def archive_stats(self):
        """Return a dict of archive statistics."""
        total = self.total_images
        digits = len(str(total))
        return {
            "resolution": f"{self.width}x{self.height}",
            "colors_per_channel": self.colors_per_channel,
            "total_palette_colors": self.palette_size,
            "total_pixels": self.total_pixels,
            "total_possible_images": total,
            "total_images_digits": digits,
            "address_space_bits": total.bit_length(),
            "key": self.key,
        }


# =============================================================================
# CLI Interface
# =============================================================================

def cmd_browse(args):
    """Retrieve an image from the archive by address."""
    archive = BabelImageArchive(args.width, args.height, args.colors, args.key)
    img = archive.address_to_image(args.address)

    output = args.output or f"babel_{args.address[:20]}.png"
    if args.scale > 1:
        img = img.resize(
            (archive.width * args.scale, archive.height * args.scale),
            Image.NEAREST,
        )
    img.save(output)
    print(f"Image saved to: {output}")
    print(f"Address: {args.address}")


def cmd_search(args):
    """Find the address of an input image."""
    archive = BabelImageArchive(args.width, args.height, args.colors, args.key)

    img = Image.open(args.image)
    address = archive.image_to_address(img)

    print(f"Image:   {args.image}")
    print(f"Address: {address}")
    print(f"Address length: {len(address)} characters")

    if args.verify:
        reconstructed = archive.address_to_image(address)
        verify_path = args.output or f"babel_verify_{Path(args.image).stem}.png"
        if args.scale > 1:
            reconstructed = reconstructed.resize(
                (archive.width * args.scale, archive.height * args.scale),
                Image.NEAREST,
            )
        reconstructed.save(verify_path)
        print(f"Verified reconstruction saved to: {verify_path}")


def cmd_random(args):
    """Generate random images from the archive."""
    archive = BabelImageArchive(args.width, args.height, args.colors, args.key)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(args.count):
        address = archive.random_address()
        img = archive.address_to_image(address)
        if args.scale > 1:
            img = img.resize(
                (archive.width * args.scale, archive.height * args.scale),
                Image.NEAREST,
            )

        filename = output_dir / f"babel_random_{i:04d}.png"
        img.save(filename)
        print(f"[{i + 1}/{args.count}] {filename}  address={address[:40]}...")

    print(f"\nGenerated {args.count} random images in: {output_dir}/")


def cmd_stats(args):
    """Display archive statistics."""
    archive = BabelImageArchive(args.width, args.height, args.colors, args.key)
    stats = archive.archive_stats()

    print("=" * 60)
    print("  BABEL UNIVERSAL IMAGE ARCHIVE — Statistics")
    print("=" * 60)
    print(f"  Resolution:            {stats['resolution']}")
    print(f"  Colors per channel:    {stats['colors_per_channel']}")
    print(f"  Total palette colors:  {stats['total_palette_colors']}")
    print(f"  Total pixels/image:    {stats['total_pixels']}")
    print(f"  Address space:         {stats['address_space_bits']} bits")
    print(f"  Total possible images: 10^{stats['total_images_digits'] - 1}+ "
          f"({stats['total_images_digits']} digits)")
    print(f"  Archive key:           {stats['key']}")
    print("=" * 60)
    print()
    print("  This archive contains EVERY possible image at the above")
    print("  resolution and color depth. Every photograph ever taken,")
    print("  every painting, every frame of every film — they are all")
    print("  here, along with countless images never before seen.")
    print("=" * 60)


def cmd_demo(args):
    """Run an interactive demo: create a test image, search, and verify."""
    archive = BabelImageArchive(args.width, args.height, args.colors, args.key)
    stats = archive.archive_stats()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  BABEL UNIVERSAL IMAGE ARCHIVE — Demo")
    print("=" * 60)
    print(f"  Resolution: {stats['resolution']}  |  Palette: {stats['total_palette_colors']} colors")
    print(f"  Total images: 10^{stats['total_images_digits'] - 1}+")
    print()

    # Step 1: Create a simple gradient test image
    print("[1/4] Creating test gradient image...")
    test_img = Image.new("RGB", (args.width, args.height))
    px = test_img.load()
    for y in range(args.height):
        for x in range(args.width):
            r = int(255 * x / max(args.width - 1, 1))
            g = int(255 * y / max(args.height - 1, 1))
            b = 128
            px[x, y] = (r, g, b)

    test_path = output_dir / "demo_original.png"
    scaled = test_img.resize((args.width * args.scale, args.height * args.scale), Image.NEAREST)
    scaled.save(test_path)
    print(f"       Saved: {test_path}")

    # Step 2: Search for its address
    print("[2/4] Searching archive for image address...")
    address = archive.image_to_address(test_img)
    print(f"       Address: {address[:60]}{'...' if len(address) > 60 else ''}")
    print(f"       Address length: {len(address)} characters")

    # Step 3: Retrieve from address
    print("[3/4] Retrieving image from address...")
    retrieved = archive.address_to_image(address)
    retrieved_path = output_dir / "demo_retrieved.png"
    retrieved_scaled = retrieved.resize(
        (args.width * args.scale, args.height * args.scale), Image.NEAREST
    )
    retrieved_scaled.save(retrieved_path)
    print(f"       Saved: {retrieved_path}")

    # Step 4: Verify round-trip
    print("[4/4] Verifying round-trip integrity...")
    # Quantize original for fair comparison
    raw = test_img.convert("RGB").tobytes()
    quantized_original = []
    for i in range(0, len(raw), 3):
        r, g, b = raw[i], raw[i + 1], raw[i + 2]
        idx = archive._color_to_index(r, g, b)
        quantized_original.append(archive._index_to_color(idx))

    retrieved_pixels = [
        retrieved.getpixel((x, y))
        for y in range(archive.height)
        for x in range(archive.width)
    ]
    match = quantized_original == retrieved_pixels
    print(f"       Round-trip match: {'PASS' if match else 'FAIL'}")

    # Step 5: Generate a few random images
    print()
    print("Bonus: Generating 5 random images from the archive...")
    for i in range(5):
        addr = archive.random_address()
        img = archive.address_to_image(addr)
        img_scaled = img.resize(
            (args.width * args.scale, args.height * args.scale), Image.NEAREST
        )
        path = output_dir / f"demo_random_{i}.png"
        img_scaled.save(path)
        print(f"  [{i + 1}] {path}")

    print()
    print("Demo complete! Check the output directory for results.")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Babel Universal Image Archive Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s stats                          Show archive statistics
  %(prog)s demo                           Run interactive demo
  %(prog)s browse <address>               Retrieve image by address
  %(prog)s search image.png               Find address of an image
  %(prog)s search image.png --verify      Find address and verify round-trip
  %(prog)s random --count 10              Generate 10 random images
        """,
    )

    # Global options
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH,
                        help=f"Image width in pixels (default: {DEFAULT_WIDTH})")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT,
                        help=f"Image height in pixels (default: {DEFAULT_HEIGHT})")
    parser.add_argument("--colors", type=int, default=DEFAULT_COLORS,
                        help=f"Colors per channel (default: {DEFAULT_COLORS})")
    parser.add_argument("--key", type=str, default=DEFAULT_KEY,
                        help="Archive key for address shuffling (default: 'babel')")
    parser.add_argument("--scale", type=int, default=16,
                        help="Scale factor for output images (default: 16)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # browse
    p_browse = subparsers.add_parser("browse", help="Retrieve image by address")
    p_browse.add_argument("address", help="Base-62 image address")
    p_browse.add_argument("-o", "--output", help="Output file path")

    # search
    p_search = subparsers.add_parser("search", help="Find address of an image")
    p_search.add_argument("image", help="Path to input image")
    p_search.add_argument("-o", "--output", help="Output path for verified image")
    p_search.add_argument("--verify", action="store_true",
                          help="Reconstruct and save the image from its address")

    # random
    p_random = subparsers.add_parser("random", help="Generate random images")
    p_random.add_argument("--count", type=int, default=5,
                          help="Number of random images (default: 5)")
    p_random.add_argument("--output-dir", default="babel_random",
                          help="Output directory (default: babel_random)")

    # stats
    subparsers.add_parser("stats", help="Show archive statistics")

    # demo
    p_demo = subparsers.add_parser("demo", help="Run interactive demo")
    p_demo.add_argument("--output-dir", default="babel_demo",
                        help="Output directory (default: babel_demo)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "browse": cmd_browse,
        "search": cmd_search,
        "random": cmd_random,
        "stats": cmd_stats,
        "demo": cmd_demo,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
