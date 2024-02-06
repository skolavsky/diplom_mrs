# settings_common.py
from pathlib import Path
from decouple import config

# Глобальные переменные в приложении
FIO_RE_VALIDATION = "^[A-Za-zА-Яа-яЁё' -]+$"
FIO_MAX_LENGTH = 100
MAX_PRECISION_TO_FIELDS = 3
START_ADMISSION_DATE = 2023

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

STATICFILES_DIRS = [
    BASE_DIR / 'web_handler' / 'static',
    BASE_DIR / 'clients' / 'static',
]

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# white-noise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'web_handler',
    'clients',
    'simple_history',

]

SIMPLE_HISTORY_HISTORY_ID_USE_UUID = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mrs_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'clients.context_processors.add_query_params_to_context',

            ],
        },
    },
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Set session cookie age to 8 hours (in seconds)
SESSION_COOKIE_AGE = 8 * 60 * 60  # 8 hours * 60 minutes * 60 seconds
LOGIN_URL = '/login/'

WSGI_APPLICATION = 'mrs_proj.wsgi.application'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', #.AllowAny | .IsAuthenticated | .IsAdminUser
    ],
    # API requests limitation
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/day',
        'user': '60/min'
    },
}
