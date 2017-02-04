import os

## Common options to all scrapers

DISTRICTS = os.getenv('DISTRICTS', [])
if isinstance(DISTRICTS, list) == False:
    DISTRICTS = [int(e) for e in DISTRICTS.split(',')]
BLACKLISTED_WORDS = os.getenv('BLACKLISTED_WORDS', [])
if isinstance(BLACKLISTED_WORDS, list) == False:
    BLACKLISTED_WORDS = [e.strip() for e in BLACKLISTED_WORDS.split(',')]

MIN_PRICE = int(os.getenv('MIN_PRICE', 0))
MAX_PRICE = int(os.getenv('MAX_PRICE', 0))
MIN_PRICE_PER_SURFACE_UNIT = int(os.getenv('MIN_PRICE_PER_SURFACE_UNIT', 0))
MIN_SIZE = int(os.getenv('MIN_SIZE', 0))
MAX_BUILDING_YEAR = int(os.getenv('BUILDING_MAX_YEAR', 1950))

## System settings

SLEEP_INTERVAL = int(os.getenv('SLEEP_INTERVAL', 60 * 40)) # 40 minutes

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///offers.db')

## Slack integration

# Which slack channel to post the listings into.
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '')

# The token that allows us to connect to slack.
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', '')
SLACK_BOT_NAME = os.getenv('SLACK_BOT_NAME', '')
SLACK_BOT_ICON = os.getenv('SLACK_BOT_ICON', '')

## Pap specifics

PAP_DEVICE_GSF = os.getenv('PAP_DEVICE_GSF', '')

# Any private settings are imported here.
try:
    from private import *
except Exception:
    pass

# Any external private settings are imported from here.
try:
    from config.private import *
except Exception:
    pass
