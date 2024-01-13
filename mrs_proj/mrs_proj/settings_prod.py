from .settings_common import *   #NOSONAR
# SECURITY WARNING: don't run with debug turned on in production!
import os

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOST', '').split(', ')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
