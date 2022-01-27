import os

senv = os.environ.get('DH_SETTINGS_ENVIRONMENT', 'dev')
if senv == 'dev':
    from .dev import *
elif senv == 'prod':
    from .prod import *
else:
    raise ImportError("Couldn't determine which settings environment to load. Make sure that the DH_SETTINGS_ENVIRONMENT environment variable is set correctly.")