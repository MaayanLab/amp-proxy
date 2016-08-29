"""Handles application-wide configurations.
"""

from configparser import ConfigParser
import os


config = ConfigParser()
config.read('/app/app/config.ini')

MARATHON_URL = config.get('marathon', 'url')
MARATHON_USER = config.get('marathon', 'username')
MARATHON_PASSWORD = config.get('marathon', 'password')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
