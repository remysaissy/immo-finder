import os

# Content filtering
DISTRICTS = os.getenv('DISTRICTS', [75001,75002,75003,75004,75005,75006,75007,75008,75009,75010,75011,75012,75013,75014,75015,75016,75017,75018,75019,75020])
if not isinstance(DISTRICTS, list):
    DISTRICTS = [e.strip() for e in DISTRICTS.split(',')]

# Pricing filtering
MAX_PRICE = int(os.getenv('MAX_PRICE', 200000))

# Surface filtering
MIN_SIZE = int(os.getenv('MIN_SIZE', 20))

