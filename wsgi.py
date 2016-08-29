"""This script only runs in production (Docker container) when boot.sh is
executed.
"""

from app.app import app as application
