import uvicorn
import os
from dotenv import load_dotenv
import structlog
import logging
from pythonjsonlogger import jsonlogger
from app import create_app

# Load environment variables
load_dotenv()

# Configure logging
def setup_logging():
    """Configure structured logging for the application."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(log_level)),
        logger_factory=structlog.PrintLoggerFactory(),
    )

    # Configure JSON logging for uvicorn
    logger = logging.getLogger("uvicorn")
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter())
    logger.addHandler(handler)

if __name__ == "__main__":
    setup_logging()
    
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5555'))
    workers = int(os.getenv('WORKERS', '4'))
    reload = os.getenv('FLASK_ENV') == 'development'
    
    # Run with uvicorn
    uvicorn.run(
        "wsgi:app",
        host=host,
        port=port,
        workers=workers if not reload else None,
        reload=reload,
        log_level=os.getenv('LOG_LEVEL', 'info').lower()
    )

