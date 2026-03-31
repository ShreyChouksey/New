"""Application configuration."""

import os


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "babel-archive-secret-key-change-in-prod")

    # Archive parameters
    BABEL_WIDTH = int(os.environ.get("BABEL_WIDTH", 16))
    BABEL_HEIGHT = int(os.environ.get("BABEL_HEIGHT", 16))
    BABEL_COLORS = int(os.environ.get("BABEL_COLORS", 8))
    BABEL_KEY = os.environ.get("BABEL_KEY", "babel")
    BABEL_COLOR_MODE = os.environ.get("BABEL_COLOR_MODE", "rgb")
    BABEL_SHUFFLE_MODE = os.environ.get("BABEL_SHUFFLE_MODE", "xor")
    BABEL_SCALE = int(os.environ.get("BABEL_SCALE", 16))

    # Upload limits
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # Gallery
    GALLERY_ROOMS_PER_PAGE = 10


class DevConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProdConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", None)


config_map = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig,
}
