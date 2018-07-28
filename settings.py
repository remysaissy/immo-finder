
# Load default config.
try:
    from config import *
except Exception:
    pass

# Config overrides.
try:
    from config_private import *
except Exception:
    pass
