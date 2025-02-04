from flask import Flask
from .config import Config
from .project_creator import project_creator
from .logging_config import configure_logging
from asgiref.wsgi import WsgiToAsgi

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure logging
    configure_logging()
    
    # Register blueprints
    app.register_blueprint(project_creator)
    
    # Convert WSGI app to ASGI
    asgi_app = WsgiToAsgi(app)
    return asgi_app 