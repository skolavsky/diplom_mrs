# settings.py

import os

DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *
