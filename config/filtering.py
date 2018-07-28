import os

# Content filtering
BLACKLISTED_WORDS = os.getenv('BLACKLISTED_WORDS', [])
if isinstance(BLACKLISTED_WORDS, list) == False:
    BLACKLISTED_WORDS = [e.strip() for e in BLACKLISTED_WORDS.split(',')]

# Pricing filtering
MIN_PRICE = int(os.getenv('MIN_PRICE', 0))
MAX_PRICE = int(os.getenv('MAX_PRICE', 0))
MIN_PRICE_PER_SURFACE_UNIT = int(os.getenv('MIN_PRICE_PER_SURFACE_UNIT', 0))

# Surface filtering
MIN_SIZE = int(os.getenv('MIN_SIZE', 0))

# Building characteristics filtering
MAX_BUILDING_YEAR = int(os.getenv('BUILDING_MAX_YEAR', 0))
