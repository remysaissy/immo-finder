import os

PAP_SEARCH_TYPE = os.getenv('PAP_SEARCH_TYPE', [])
if isinstance(PAP_SEARCH_TYPE, list) == False:
    PAP_SEARCH_TYPE = [e.strip() for e in PAP_SEARCH_TYPE.split(',')]

PAP_SEARCH_LOCATION = os.getenv('PAP_SEARCH_LOCATION', '')

