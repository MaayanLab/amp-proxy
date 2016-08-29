"""Loads and runs application in production.
"""

from app.app import app

app.debug = False
app.run(port=52496, host='0.0.0.0')
