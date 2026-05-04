import os
from dotenv import load_dotenv

load_dotenv()

# Apify Configuration
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')

# Default Search Parameters
DEFAULT_LOCATION = os.getenv('DEFAULT_LOCATION', 'Tel Aviv')
MIN_PRICE = int(os.getenv('MIN_PRICE', 1000))
MAX_PRICE = int(os.getenv('MAX_PRICE', 5000))
MIN_ROOMS = int(os.getenv('MIN_ROOMS', 1))
MAX_ROOMS = int(os.getenv('MAX_ROOMS', 4))

# Output Configuration
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'csv')
SAVE_TO_FILE = os.getenv('SAVE_TO_FILE', 'true').lower() == 'true'
OUTPUT_DIR = 'data'

# Apify Actor IDs (these are the official Yad2 and Madlan scrapers on Apify)
YAD2_ACTOR_ID = 'swerve/yad2-scraper'
MADLAN_ACTOR_ID = 'swerve/madlan-scraper'

# API Configuration
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
