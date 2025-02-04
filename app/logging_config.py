import logging
import os
import structlog
from pythonjsonlogger import jsonlogger

def configure_logging():
    """Configure structured logging for the application."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Configure standard logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure JSON formatter for standard logging
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(jsonlogger.JsonFormatter())
    
    # Add handler to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(json_handler)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Create a logger instance for the application
    logger = structlog.get_logger("app")
    
    return logger

def get_logger(name):
    """Get a logger instance for the specified name."""
    return structlog.get_logger(name) 