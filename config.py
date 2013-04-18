import os

DEBUG = True

VERSION = '0.0.1'

# general
BASE_DIR = os.path.dirname(__file__)

# web app
HOST = 'localhost'
PORT = 8000
STATIC_PATH = 'static'
TEMPLATES_DIR = 'templates'

# stats parser
PLAY_BY_PLAY_URL = 'http://www.nhl.com/scores/htmlreports/20122013/PL02{game_id:04d}.HTM'
PLAY_BY_PLAY_DIR = 'playbyplay_reports'
DATA_DIR = 'generated_reports'
