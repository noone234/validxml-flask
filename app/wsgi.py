# wsgi.py

import sys
import logging
logging.basicConfig(stream=sys.stderr)

from app import create_app
application = create_app()
