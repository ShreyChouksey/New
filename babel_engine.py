"""
Babel Universal Image Archive — Core Engine

A reversible mapping between unique addresses and images. Every possible image
at a configured resolution and color depth exists in the archive and can be
retrieved by its address. No images are stored — they are computed on demand.
"""

import base64
import enum
import hashlib
import hmac
import io
import math
import random
import struct
from PIL import Image


# =============================================================================
# Constants
# =============================================================================

BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE62_SET = frozenset(BASE62_CHARS)


# =============================================================================
# Enums
# =============================================================================

class ColorMode(enum.Enum):
    RGB = "rgb"
    GRAYSCALE = "grayscale"
    BW = "bw"


class ShuffleMode(enum.Enum):
    XOR = "xor"
    FEISTEL = "feistel"


# =============================================================================
# Exceptions
# =============================================================================

class BabelError(Exception):
    """Base exception for Babel Image Archive."""
    pass


class InvalidAddressError(BabelError):
    """Raised when an address contains invalid characters."""
    pass


class AddressOutOfRangeError(BabelError):
    """Raised when an address maps to a value outside the archive."""
    pass


# =============================================================================
# Address Encoding
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
        idx = BASE62_CHARS.find(ch)
        if idx < 0:
            raise InvalidAddressError(f"Invalid base-62 character: '{ch}'")
        n = n * 62 + idx
    return n


def is_valid_address(address):
    """Check if a string is a valid base-62 address."""
    return bool(address) and all(ch in BASE62_SET for ch in address)


# =============================================================================
# Shuffle Algorithms
# =============================================================================

def _derive_keystream(key, length):
    """Derive a deterministic keystream from a string key using SHA-256 chaining."""
    keystream = bytearray()
    counter = 0
    while len(keystream) < length:
        h = hashlib.sha256(f"{key}:{counter}".encode()).digest()
        keystream.extend(h)
        counter += 1
    return bytes(keystream[:length])


def _xor_shuffle(data_int, key, byte_length):
    """XOR an integer with a key-derived stream."""
    data_bytes = data_int.to_bytes(byte_length, byteorder="big")
    keystream = _derive_keystream(key, byte_length)
    xored = bytes(a ^ b for a, b in zip(data_bytes, keystream))
    return int.from_bytes(xored, byteorder="big")


def _feistel_round(value, round_key, half_bits):
    """One round of a Feistel cipher using HMAC-SHA256."""
    val_bytes = value.to_bytes(max(1, (half_bits + 7) // 8), byteorder="big")
    h = hmac.new(round_key, val_bytes, hashlib.sha256).digest()
    return int.from_bytes(h, byteorder="big") & ((1 << half_bits) - 1)


def _feistel_encrypt(plaintext, key, total_images, num_rounds=8):
    """
    Format-Preserving Encryption using a Feistel network with cycle-walking.
    Guarantees a true permutation over [0, total_images).
    """
    total_bits = total_images.bit_length()
    half_bits = (total_bits + 1) // 2
    mask = (1 << half_bits) - 1

    # Derive round keys
    round_keys = []
    for i in range(num_rounds):
        rk = hashlib.sha256(f"{key}:feistel_round:{i}".encode()).digest()
        round_keys.append(rk)

    value = plaintext
    # Cycle-walking: keep encrypting until result is in range
    while True:
        left = (value >> half_bits) & mask
        right = value & mask

        for rk in round_keys:
            new_left = right
            new_right = left ^ _feistel_round(right, rk, half_bits)
            new_right &= mask
            left = new_left
            right = new_right

        result = (left << half_bits) | right
        if result < total_images:
            return result
        # Cycle-walk: use the out-of-range result as new input
        value = result


def _feistel_decrypt(ciphertext, key, total_images, num_rounds=8):
    """Reverse Feistel encryption (decryption)."""
    total_bits = total_images.bit_length()
    half_bits = (total_bits + 1) // 2
    mask = (1 << half_bits) - 1

    round_keys = []
    for i in range(num_rounds):
        rk = hashlib.sha256(f"{key}:feistel_round:{i}".encode()).digest()
        round_keys.append(rk)

    value = ciphertext
    while True:
        left = (value >> half_bits) & mask
        right = value & mask

        for rk in reversed(round_keys):
            new_right = left
            new_left = right ^ _feistel_round(left, rk, half_bits)
            new_left &= mask
            left = new_left
            right = new_right

        result = (left << half_bits) | right
        if result < total_images:
            return result
        value = result


# =============================================================================
# Gallery Spatial Addressing
# =============================================================================

class GalleryLocation:
    """Represents a location in the archive's spatial hierarchy."""

    def __init__(self, room, wall, shelf, position):
        self.room = room
        self.wall = wall
        self.shelf = shelf
        self.position = position

    def __repr__(self):
        return (f"GalleryLocation(room={self.room}, wall={self.wall}, "
                f"shelf={self.shelf}, position={self.position})")

    def to_dict(self):
        return {
            "room": self.room,
            "wall": self.wall,
            "shelf": self.shelf,
            "position": self.position,
        }


# =============================================================================
# Core Archive Engine
# =============================================================================

class BabelImageArchive:
    """
    The Universal Image Archive.

    Every possible image of the configured resolution and color depth exists
    within this archive and can be retrieved by its unique address.
    """

    # Gallery layout constants
    WALLS_PER_ROOM = 4
    SHELVES_PER_WALL = 5
    IMAGES_PER_SHELF = 8

    def __init__(self, width=16, height=16, colors_per_channel=8,
                 color_mode=ColorMode.RGB, key="babel",
                 shuffle_mode=ShuffleMode.XOR):
        self.width = width
        self.height = height
        self.colors_per_channel = colors_per_channel
        self.color_mode = color_mode
        self.key = key
        self.shuffle_mode = shuffle_mode
        self.total_pixels = width * height

        # Compute palette size based on color mode
        if color_mode == ColorMode.BW:
            self.palette_size = 2
        elif color_mode == ColorMode.GRAYSCALE:
            self.palette_size = colors_per_channel
        else:  # RGB
            self.palette_size = colors_per_channel ** 3

        # Total number of possible images
        self.total_images = self.palette_size ** self.total_pixels

        # Byte length needed to represent the largest image index
        self.byte_length = max(1, math.ceil(self.total_images.bit_length() / 8))

        # Quantization step for mapping palette index -> 0-255
        if colors_per_channel > 1:
            self.quant_step = 255 / (colors_per_channel - 1)
        else:
            self.quant_step = 255

        # Gallery derived values
        self.images_per_room = (self.WALLS_PER_ROOM *
                                self.SHELVES_PER_WALL *
                                self.IMAGES_PER_SHELF)

    # -------------------------------------------------------------------------
    # Color Conversion
    # -------------------------------------------------------------------------

    def _index_to_color(self, idx):
        """Convert a palette index to a color value."""
        if self.color_mode == ColorMode.BW:
            return (255 if idx else 0,)
        elif self.color_mode == ColorMode.GRAYSCALE:
            v = min(int(round(idx * self.quant_step)), 255)
            return (v,)
        else:
            cpc = self.colors_per_channel
            b = idx % cpc
            g = (idx // cpc) % cpc
            r = (idx // (cpc * cpc)) % cpc
            return (
                min(int(round(r * self.quant_step)), 255),
                min(int(round(g * self.quant_step)), 255),
                min(int(round(b * self.quant_step)), 255),
            )

    def _color_to_index(self, *channels):
        """Convert color channels to the nearest palette index."""
        if self.color_mode == ColorMode.BW:
            return 1 if channels[0] > 127 else 0
        elif self.color_mode == ColorMode.GRAYSCALE:
            cpc = self.colors_per_channel
            return min(round(channels[0] / self.quant_step), cpc - 1)
        else:
            cpc = self.colors_per_channel
            r, g, b = channels[0], channels[1], channels[2]
            ri = min(round(r / self.quant_step), cpc - 1)
            gi = min(round(g / self.quant_step), cpc - 1)
            bi = min(round(b / self.quant_step), cpc - 1)
            return int(ri * cpc * cpc + gi * cpc + bi)

    def _pil_mode(self):
        """Return the PIL image mode for the current color mode."""
        if self.color_mode in (ColorMode.BW, ColorMode.GRAYSCALE):
            return "L"
        return "RGB"

    # -------------------------------------------------------------------------
    # Integer <-> Pixel Conversion
    # -------------------------------------------------------------------------

    def _int_to_pixels(self, n):
        """Convert an integer to a list of palette indices."""
        pixels = []
        for _ in range(self.total_pixels):
            pixels.append(int(n % self.palette_size))
            n //= self.palette_size
        return list(reversed(pixels))

    def _pixels_to_int(self, pixels):
        """Convert a list of palette indices to an integer."""
        n = 0
        for p in pixels:
            n = n * self.palette_size + p
        return n

    # -------------------------------------------------------------------------
    # Shuffle / Unshuffle
    # -------------------------------------------------------------------------

    def _shuffle(self, image_int):
        """Map image index -> address index (forward direction)."""
        if self.shuffle_mode == ShuffleMode.FEISTEL:
            return _feistel_encrypt(image_int, self.key, self.total_images)
        else:
            result = _xor_shuffle(image_int, self.key, self.byte_length)
            return result % self.total_images

    def _unshuffle(self, address_int):
        """Map address index -> image index (reverse direction)."""
        if self.shuffle_mode == ShuffleMode.FEISTEL:
            return _feistel_decrypt(address_int, self.key, self.total_images)
        else:
            result = _xor_shuffle(address_int, self.key, self.byte_length)
            return result % self.total_images

    # -------------------------------------------------------------------------
    # Core API
    # -------------------------------------------------------------------------

    def validate_address(self, address):
        """Validate an address string. Raises on invalid."""
        if not address:
            raise InvalidAddressError("Address cannot be empty")
        if not is_valid_address(address):
            bad = [ch for ch in address if ch not in BASE62_SET]
            raise InvalidAddressError(
                f"Invalid characters in address: {bad[:5]}"
            )
        raw_int = base62_to_int(address)
        if raw_int >= self.total_images:
            raise AddressOutOfRangeError(
                f"Address out of range. Max address length for this archive: "
                f"~{len(int_to_base62(self.total_images - 1))} characters"
            )

    def address_to_image(self, address):
        """Retrieve a PIL Image from the archive by its address."""
        self.validate_address(address)
        raw_int = base62_to_int(address)
        image_int = self._unshuffle(raw_int)
        pixels = self._int_to_pixels(image_int)

        pil_mode = self._pil_mode()
        img = Image.new(pil_mode, (self.width, self.height))
        img_pixels = img.load()

        for i, p in enumerate(pixels):
            x = i % self.width
            y = i // self.width
            color = self._index_to_color(p)
            img_pixels[x, y] = color[0] if pil_mode == "L" else color

        return img

    def image_to_address(self, img):
        """Find the address of an image in the archive."""
        pil_mode = self._pil_mode()
        img = img.convert(pil_mode if pil_mode == "L" else "RGB")
        img = img.resize((self.width, self.height), Image.LANCZOS)

        pixels = []
        for y in range(self.height):
            for x in range(self.width):
                px = img.getpixel((x, y))
                if pil_mode == "L":
                    pixels.append(self._color_to_index(px))
                else:
                    pixels.append(self._color_to_index(*px))

        image_int = self._pixels_to_int(pixels)
        raw_int = self._shuffle(image_int)
        return int_to_base62(raw_int)

    def random_address(self):
        """Generate a random valid address."""
        n = random.randint(0, min(self.total_images - 1, (1 << 2048) - 1))
        return int_to_base62(n)

    def random_image(self):
        """Generate a random image and return (address, PIL Image)."""
        address = self.random_address()
        return address, self.address_to_image(address)

    # -------------------------------------------------------------------------
    # Image Rendering Helpers
    # -------------------------------------------------------------------------

    def address_to_png_bytes(self, address, scale=1):
        """Render an image to PNG bytes (for web serving)."""
        img = self.address_to_image(address)
        if scale > 1:
            img = img.resize(
                (self.width * scale, self.height * scale),
                Image.NEAREST,
            )
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    def address_to_base64(self, address, scale=1):
        """Render an image as a base64-encoded PNG string."""
        png_bytes = self.address_to_png_bytes(address, scale)
        return base64.b64encode(png_bytes).decode("ascii")

    def image_to_quantized_base64(self, img, scale=1):
        """Quantize an input image to archive colors and return as base64 PNG."""
        address = self.image_to_address(img)
        return address, self.address_to_base64(address, scale)

    # -------------------------------------------------------------------------
    # Gallery / Spatial Navigation
    # -------------------------------------------------------------------------

    def address_to_location(self, address):
        """Convert an address to a gallery location (room/wall/shelf/position)."""
        self.validate_address(address)
        idx = base62_to_int(address)
        position = idx % self.IMAGES_PER_SHELF
        idx //= self.IMAGES_PER_SHELF
        shelf = idx % self.SHELVES_PER_WALL
        idx //= self.SHELVES_PER_WALL
        wall = idx % self.WALLS_PER_ROOM
        room = idx // self.WALLS_PER_ROOM
        return GalleryLocation(room, wall, shelf, position)

    def location_to_address(self, room, wall, shelf, position):
        """Convert a gallery location back to an address."""
        idx = room
        idx = idx * self.WALLS_PER_ROOM + wall
        idx = idx * self.SHELVES_PER_WALL + shelf
        idx = idx * self.IMAGES_PER_SHELF + position
        if idx >= self.total_images:
            raise AddressOutOfRangeError("Gallery location is out of range")
        return int_to_base62(idx)

    def get_shelf_images(self, room, wall, shelf):
        """Get all image addresses on a given shelf."""
        addresses = []
        for pos in range(self.IMAGES_PER_SHELF):
            try:
                addr = self.location_to_address(room, wall, shelf, pos)
                addresses.append(addr)
            except AddressOutOfRangeError:
                break
        return addresses

    def get_neighbors(self, address, offsets=None):
        """
        Get neighboring addresses at specified offsets.
        Returns list of (offset, address) tuples.
        """
        if offsets is None:
            offsets = [-100, -10, -5, -1, 0, 1, 5, 10, 100]

        self.validate_address(address)
        center = base62_to_int(address)
        neighbors = []
        for offset in offsets:
            idx = center + offset
            if 0 <= idx < self.total_images:
                neighbors.append((offset, int_to_base62(idx)))
        return neighbors

    def total_rooms(self):
        """Total number of gallery rooms."""
        total = self.total_images
        per_room = self.images_per_room
        return (total + per_room - 1) // per_room

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    def archive_stats(self):
        """Return comprehensive archive statistics."""
        total = self.total_images
        total_str = str(total)
        digits = len(total_str)
        max_addr = int_to_base62(total - 1)

        return {
            "resolution": f"{self.width}x{self.height}",
            "width": self.width,
            "height": self.height,
            "color_mode": self.color_mode.value,
            "colors_per_channel": self.colors_per_channel,
            "total_palette_colors": self.palette_size,
            "total_pixels": self.total_pixels,
            "total_possible_images": total,
            "total_images_digits": digits,
            "total_images_scientific": f"{total_str[0]}.{total_str[1:6]}... x 10^{digits - 1}" if digits > 6 else str(total),
            "address_space_bits": total.bit_length(),
            "max_address_length": len(max_addr),
            "shuffle_mode": self.shuffle_mode.value,
            "key": self.key,
            "gallery_walls_per_room": self.WALLS_PER_ROOM,
            "gallery_shelves_per_wall": self.SHELVES_PER_WALL,
            "gallery_images_per_shelf": self.IMAGES_PER_SHELF,
            "total_gallery_rooms": str(self.total_rooms()),
        }
