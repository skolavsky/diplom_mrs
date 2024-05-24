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

    'axes.backends.AxesStandaloneBackend',  # Для axes чтобы отслеживать неправильные входы
    'django.contrib.auth.backends.ModelBackend',
    'web_handler.authentication.EmailAuthBackend',
]

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'account.apps.AccountConfig',  # own application
    'web_handler.apps.WebHandlerConfig',  # own application
    'clients.apps.ClientsConfig',  # own application
    'blog.apps.BlogConfig',  # own application
    "unfold",  # before django.contrib.admin
    'axes',  # приложение для отслеживания неудачных попыток взлома
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.staticfiles',  # последнее приложение для двухфаторной аутентификации
    'crispy_forms',  # приложение для bootstrap4 форм
    'crispy_bootstrap4',  # или 'crispy_bootstrap5' в зависимости от используемой версии
    'ratelimit',  # приложение для ограничивания слишком большого кол-ва запросов к представлению
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_ckeditor_5',  # приложение для редактирования текста
    'rest_framework',
    'easy_thumbnails',  # приложение для создания миниатюр изображений
    'django.contrib.sitemaps',  # приложение для карты сайт
    'django.contrib.postgres',  # приложение для работы с базой postgresql
    'simple_history',  # приложение для истории(Clients)
    'taggit',  # приложение для тегов(используется в блоге)
    'django_otp',  # приложения для двухфаторной аутентификации
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'two_factor',
    'django.contrib.sites',
    'robots',  # приложение для создания файла с информацией для поисковых машин
    "django_unicorn",  # required for Django to register urls and templatetags
    'django_cryptography',  # для шифрования полей модели

]

SITE_ID = 1  # нужно для карты сайтов. admin/sites/site

CRISPY_TEMPLATE_PACK = 'bootstrap4'  # пакет для рендеринга форм

FIELD_ENCRYPTION_KEY = config('FIELD_ENCRYPTION_KEY')


# настройки для axes
AXES_FAILURE_LIMIT = 10  # кол-во неудачных попыток входа
AXES_COOLOFF_TIME = 1  # Cool-off period in hours
AXES_LOCK_OUT_AT_FAILURE = True  # Блокировать после неудачных попыток

CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = False

customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
        'language': 'ru',

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                    'code', 'subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable', ],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',
                               'tableProperties', 'tableCellProperties'],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

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
    'axes.middleware.AxesMiddleware',  # для axes
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
