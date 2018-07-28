import os

## System settings

SLEEP_INTERVAL = int(os.getenv('SLEEP_INTERVAL', 60 * 40)) # 40 minutes
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///offers.db')

# DEBUG, INFO, WARNING, ERROR
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
