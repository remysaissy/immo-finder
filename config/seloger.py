import os

SELOGER_SEARCH_TYPE = os.getenv('SELOGER_SEARCH_TYPE', [])
if isinstance(SELOGER_SEARCH_TYPE, list) == False:
    SELOGER_SEARCH_TYPE = [e.strip() for e in SELOGER_SEARCH_TYPE.split(',')]

SELOGER_SEARCH_PROJECTS = os.getenv('SELOGER_SEARCH_PROJECTS', [])
if isinstance(SELOGER_SEARCH_PROJECTS, list) == False:
    SELOGER_SEARCH_PROJECTS = [e.strip() for e in SELOGER_SEARCH_PROJECTS.split(',')]

SELOGER_SEARCH_NATURES = os.getenv('SELOGER_SEARCH_NATURES', [])
if isinstance(SELOGER_SEARCH_TYPE, list) == False:
    SELOGER_SEARCH_NATURES = [e.strip() for e in SELOGER_SEARCH_NATURES.split(',')]


SELOGER_SEARCH_LOCATION = os.getenv('SELOGER_SEARCH_LOCATION', [])
if isinstance(SELOGER_SEARCH_LOCATION, list) == False:
    SELOGER_SEARCH_LOCATION = [e.strip() for e in SELOGER_SEARCH_LOCATION.split(',')]
