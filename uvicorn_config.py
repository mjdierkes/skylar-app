import multiprocessing
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Server configuration
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '5000')}"
workers = int(os.getenv('WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging
loglevel = os.getenv('LOG_LEVEL', 'info')
accesslog = '-'
errorlog = '-'

# SSL (uncomment and configure if using HTTPS)
# keyfile = 'path/to/keyfile'
# certfile = 'path/to/certfile'

# Process naming
proc_name = 'ios-project-generator'

# Timeout configuration
timeout = 120
keepalive = 5

# Development settings
reload = os.getenv('FLASK_ENV') == 'development'
reload_engine = 'auto'

# Security headers
forwarded_allow_ips = '*'