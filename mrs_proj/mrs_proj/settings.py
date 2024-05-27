# settings.py
from decouple import config

DJANGO_ENV = config('DJANGO_ENV', 'dev')

# settings_dev.py или settings_prod.py
ALLOWED_HOSTS = ['*']

if DJANGO_ENV == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *
