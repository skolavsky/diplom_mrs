# settings_common.py
import os
from pathlib import Path

from decouple import config

CKEDITOR_UPLOAD_PATH = "uploads/"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Глобальные переменные в приложении
FIO_RE_VALIDATION = "^[A-Za-zА-Яа-яЁё' -]+$"
FIO_MAX_LENGTH = 100
MAX_PRECISION_TO_FIELDS = 3
START_ADMISSION_DATE = 2023

MAX_USER_PASSWORD_AGE = 30  # в днях. срок годности пароля

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # получать письма в консоль

# доступ к микросервису
FORECAST_URL = os.environ.get('FORECAST_URL', 'http://localhost:8888/test/')

SITE_ID = 1  # нужно для карты сайтов. admin/sites/site

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

SECRET_KEY = config('SECRET_KEY')

STATICFILES_DIRS = [
    BASE_DIR / 'web_handler' / 'static',
    BASE_DIR / 'clients' / 'static',
]

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# white-noise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'web_handler.authentication.EmailAuthBackend',
]

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'account.apps.AccountConfig',  # own application
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',  # приложение для редактирования текста
    'ckeditor_uploader',
    'rest_framework',
    'easy_thumbnails',  # приложение для создания миниатюр изображений
    'django.contrib.sitemaps',  # приложение для карты сайт
    'django.contrib.postgres',  # приложение для работы с базой postgresql
    'simple_history',  # приложение для истории(Clients)
    'taggit',  # приложение для тегов(используется в блоге)
    'web_handler.apps.WebHandlerConfig',  # own application
    'clients.apps.ClientsConfig',  # own application
    'blog.apps.BlogConfig',  # own application

]

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 10},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

]

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
SSESION_COOKIE_SECURE = True
LOGIN_URL = '/login/'

WSGI_APPLICATION = 'mrs_proj.wsgi.application'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # .AllowAny | .IsAuthenticated | .IsAdminUser
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
