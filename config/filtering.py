import os

# Content filtering
DISTRICTS = os.getenv('DISTRICTS', [])
if not isinstance(DISTRICTS, list):
    DISTRICTS = [e.strip() for e in DISTRICTS.split(',')]

BLACKLISTED_WORDS = os.getenv('BLACKLISTED_WORDS', [])
if not isinstance(BLACKLISTED_WORDS, list):
    BLACKLISTED_WORDS = [e.strip() for e in BLACKLISTED_WORDS.split(',')]

# Pricing filtering
MIN_PRICE = int(os.getenv('MIN_PRICE', 0))
MAX_PRICE = int(os.getenv('MAX_PRICE', 0))
MIN_PRICE_PER_SURFACE_UNIT = int(os.getenv('MIN_PRICE_PER_SURFACE_UNIT', 0))

# Surface filtering
MIN_SIZE = int(os.getenv('MIN_SIZE', 0))

# Building characteristics filtering
MAX_BUILDING_YEAR = int(os.getenv('BUILDING_MAX_YEAR', 0))
