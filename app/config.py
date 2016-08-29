"""Handles application-wide configurations.
"""

from configparser import ConfigParser


config = ConfigParser()
config.read('app/config.ini')

MARATHON_URL = config.get('marathon', 'url')
MARATHON_USER = config.get('marathon', 'username')
MARATHON_PASSWORD = config.get('marathon', 'password')
