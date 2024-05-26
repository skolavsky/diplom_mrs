# SECURITY WARNING: don't run with debug turned on in production!
import os

from .settings_common import *   #NOSONAR
ALLOWED_HOSTS = ['*']


# Чтение .env файла
# Использование переменных окружения
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myuser',
        'PASSWORD': 'password',
        'HOST': 'db',  # Это имя сервиса из docker-compose.yml
        'PORT': '5432',
    }
}