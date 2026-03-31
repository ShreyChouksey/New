"""
Babel Universal Image Archive — Flask Web Application

A commercial-grade web interface for browsing, searching, and exploring
the universal image archive.
"""

import io
import math

from flask import (
    Flask, Response, abort, jsonify, redirect, render_template,
    request, url_for,
)
from PIL import Image

from babel_engine import (
    AddressOutOfRangeError, BabelImageArchive, ColorMode, InvalidAddressError,
    ShuffleMode, int_to_base62,
)
from config import config_map


def create_app(config_name="dev"):
    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, config_map["default"]))

    # Initialize archive
    color_mode_map = {"rgb": ColorMode.RGB, "grayscale": ColorMode.GRAYSCALE, "bw": ColorMode.BW}
    shuffle_mode_map = {"xor": ShuffleMode.XOR, "feistel": ShuffleMode.FEISTEL}

    archive = BabelImageArchive(
        width=app.config["BABEL_WIDTH"],
        height=app.config["BABEL_HEIGHT"],
        colors_per_channel=app.config["BABEL_COLORS"],
        color_mode=color_mode_map.get(app.config["BABEL_COLOR_MODE"], ColorMode.RGB),
        key=app.config["BABEL_KEY"],
        shuffle_mode=shuffle_mode_map.get(app.config["BABEL_SHUFFLE_MODE"], ShuffleMode.XOR),
    )
    scale = app.config["BABEL_SCALE"]

    # Make archive available to templates
    @app.context_processor
    def inject_archive_stats():
        stats = archive.archive_stats()
        return {"archive_stats": stats, "archive": archive}

    # -------------------------------------------------------------------------
    # Error Handlers
    # -------------------------------------------------------------------------

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("errors/500.html"), 500

    # -------------------------------------------------------------------------
    # Page Routes
    # -------------------------------------------------------------------------

    @app.route("/")
    def index():
        # Generate a few sample images for the landing page
        samples = []
        for _ in range(6):
            addr = archive.random_address()
            samples.append({
                "address": addr,
                "address_short": addr[:24] + "..." if len(addr) > 24 else addr,
            })
        return render_template("index.html", samples=samples)

    @app.route("/browse", methods=["GET"])
    def browse_form():
        return render_template("browse.html")

    @app.route("/browse/<address>")
    def browse(address):
        try:
            archive.validate_address(address)
        except (InvalidAddressError, AddressOutOfRangeError) as e:
            return render_template("browse.html", error=str(e), address=address), 400

        location = archive.address_to_location(address)
        neighbors = archive.get_neighbors(address, [-5, -1, 0, 1, 5])
        return render_template(
            "browse.html",
            address=address,
            address_short=address[:40] + "..." if len(address) > 40 else address,
            location=location.to_dict(),
            neighbors=[(o, a) for o, a in neighbors if o != 0],
            scale=scale,
        )

    @app.route("/search", methods=["GET", "POST"])
    def search():
        if request.method == "GET":
            return render_template("search.html")

        if "image" not in request.files:
            return render_template("search.html", error="No image file uploaded"), 400

        file = request.files["image"]
        if file.filename == "":
            return render_template("search.html", error="No file selected"), 400

        try:
            img = Image.open(io.BytesIO(file.read()))
        except Exception:
            return render_template("search.html", error="Invalid image file"), 400

        address = archive.image_to_address(img)
        return render_template(
            "search.html",
            address=address,
            address_short=address[:40] + "..." if len(address) > 40 else address,
            original_name=file.filename,
            scale=scale,
        )

    @app.route("/random")
    def random_page():
        count = min(int(request.args.get("count", 12)), 48)
        images = []
        for _ in range(count):
            addr = archive.random_address()
            images.append({
                "address": addr,
                "address_short": addr[:20] + "..." if len(addr) > 20 else addr,
            })
        return render_template("random.html", images=images, count=count)

    @app.route("/gallery")
    def gallery():
        room = int(request.args.get("room", 0))
        wall = int(request.args.get("wall", 0))

        wall = max(0, min(wall, archive.WALLS_PER_ROOM - 1))

        shelves = []
        for s in range(archive.SHELVES_PER_WALL):
            addresses = archive.get_shelf_images(room, wall, s)
            shelf_images = []
            for addr in addresses:
                shelf_images.append({
                    "address": addr,
                    "address_short": addr[:16] + "..." if len(addr) > 16 else addr,
                })
            shelves.append(shelf_images)

        return render_template(
            "gallery.html",
            room=room,
            wall=wall,
            shelves=shelves,
            walls_per_room=archive.WALLS_PER_ROOM,
            shelves_per_wall=archive.SHELVES_PER_WALL,
            scale=scale,
        )

    @app.route("/explore/<address>")
    def explore(address):
        try:
            archive.validate_address(address)
        except (InvalidAddressError, AddressOutOfRangeError) as e:
            return render_template("explore.html", error=str(e)), 400

        offsets = [-1000, -100, -10, -1, 0, 1, 10, 100, 1000]
        neighbors = archive.get_neighbors(address, offsets)
        center_idx = next((i for i, (o, _) in enumerate(neighbors) if o == 0), 0)

        return render_template(
            "explore.html",
            address=address,
            neighbors=neighbors,
            center_idx=center_idx,
            scale=scale,
        )

    @app.route("/stats")
    def stats_page():
        return render_template("stats.html")

    # -------------------------------------------------------------------------
    # Image Serving
    # -------------------------------------------------------------------------

    @app.route("/image/<address>.png")
    def serve_image(address):
        img_scale = int(request.args.get("scale", scale))
        img_scale = max(1, min(img_scale, 32))
        try:
            png_bytes = archive.address_to_png_bytes(address, scale=img_scale)
        except (InvalidAddressError, AddressOutOfRangeError):
            abort(404)
        return Response(
            png_bytes,
            mimetype="image/png",
            headers={
                "Cache-Control": "public, max-age=31536000, immutable",
            },
        )

    # -------------------------------------------------------------------------
    # REST API v1
    # -------------------------------------------------------------------------

    @app.route("/api/v1/browse/<address>")
    def api_browse(address):
        api_scale = int(request.args.get("scale", scale))
        try:
            archive.validate_address(address)
            b64 = archive.address_to_base64(address, scale=api_scale)
            location = archive.address_to_location(address)
        except (InvalidAddressError, AddressOutOfRangeError) as e:
            return jsonify({"error": str(e)}), 400

        return jsonify({
            "address": address,
            "image_base64": b64,
            "location": location.to_dict(),
            "resolution": f"{archive.width}x{archive.height}",
            "palette_size": archive.palette_size,
        })

    @app.route("/api/v1/search", methods=["POST"])
    def api_search():
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files["image"]
        try:
            img = Image.open(io.BytesIO(file.read()))
        except Exception:
            return jsonify({"error": "Invalid image file"}), 400

        address = archive.image_to_address(img)
        quantized_b64 = archive.address_to_base64(address, scale=scale)
        location = archive.address_to_location(address)

        return jsonify({
            "address": address,
            "quantized_image_base64": quantized_b64,
            "location": location.to_dict(),
        })

    @app.route("/api/v1/random")
    def api_random():
        count = min(int(request.args.get("count", 6)), 48)
        api_scale = int(request.args.get("scale", scale))
        images = []
        for _ in range(count):
            addr = archive.random_address()
            images.append({
                "address": addr,
                "image_base64": archive.address_to_base64(addr, scale=api_scale),
            })
        return jsonify({"images": images, "count": count})

    @app.route("/api/v1/stats")
    def api_stats():
        return jsonify(archive.archive_stats())

    @app.route("/api/v1/gallery/<int:room>/<int:wall>/<int:shelf>")
    def api_gallery(room, wall, shelf):
        addresses = archive.get_shelf_images(room, wall, shelf)
        images = []
        for addr in addresses:
            images.append({
                "address": addr,
                "image_url": url_for("serve_image", address=addr),
            })
        return jsonify({
            "room": room,
            "wall": wall,
            "shelf": shelf,
            "images": images,
        })

    @app.route("/api/v1/explore/<address>")
    def api_explore(address):
        try:
            archive.validate_address(address)
        except (InvalidAddressError, AddressOutOfRangeError) as e:
            return jsonify({"error": str(e)}), 400

        offsets = [-100, -10, -1, 0, 1, 10, 100]
        neighbors = archive.get_neighbors(address, offsets)
        return jsonify({
            "center": address,
            "neighbors": [{"offset": o, "address": a} for o, a in neighbors],
        })

    # Add CORS headers for API routes
    @app.after_request
    def add_cors_headers(response):
        if request.path.startswith("/api/"):
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    return app


# -------------------------------------------------------------------------
# Development Server
# -------------------------------------------------------------------------

if __name__ == "__main__":
    app = create_app("dev")
    app.run(host="0.0.0.0", port=5000, debug=True)
