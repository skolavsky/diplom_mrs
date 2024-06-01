ALLOWED_HOSTS = ['*']

DEBUG = True

# Чтение .env файла
# Использование переменных окружения
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',  # Это имя сервиса из docker-compose.yml
        'PORT': '',
    }
}
