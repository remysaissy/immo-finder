import os

BIENICI_SEARCH_LOCATION = os.getenv('BIENICI_SEARCH_LOCATION', [])
if not isinstance(BIENICI_SEARCH_LOCATION, list):
    BIENICI_SEARCH_LOCATION = [e.strip() for e in BIENICI_SEARCH_LOCATION.split(',')]

BIENICI_SEARCH_TYPE = os.getenv('BIENICI_SEARCH_TYPE', ['appartement'])
if not isinstance(BIENICI_SEARCH_TYPE, list):
    BIENICI_SEARCH_TYPE = [e.strip() for e in BIENICI_SEARCH_TYPE.split(',')]

