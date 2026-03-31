"""WSGI entry point for production deployment."""

from app import create_app

application = create_app("prod")

if __name__ == "__main__":
    application.run()
