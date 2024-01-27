# settings.py

import os
from decouple import config

DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *