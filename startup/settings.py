import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SERVICE_NAME = os.getenv("SERVICE_NAME", "cd-jenkins")
SERVICE_PORT = os.getenv("SERVICE_PORT", "80")

BASICAUTH_USER = os.getenv("BASICAUTH_USER", "rafael")
BASICAUTH_PASS = os.getenv("BASICAUTH_PASS", "rafael")
BASICAUTH_USERS = {BASICAUTH_USER: BASICAUTH_PASS}

DATA_DIR = os.getenv("DATA_DIR", os.getcwd())

SECRET_KEY = 'n8ii@f47^5x#huxxy47h7ompf1z0ik-#0b^x-6_9e1j#9@fu8g'
DEBUG = os.getenv("DEBUG", "true") == "true"
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth',
    'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles', "django_tables2",
    "widget_tweaks", "startup.proxy", 'corsheaders'
]
MIDDLEWARE = [
    'startup.proxy.basicauth.middleware.BasicAuthMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny', ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'PAGE_SIZE': 50
}

LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'startup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["startup/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'startup.wsgi.application'

DATABASES = {}
# DATABASES['default'] = dj_database_url.config(conn_max_age=600)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/database' % DATA_DIR,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'stream': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['stream'],
            'level': 'INFO',
        },
        'startup': {
            'handlers': ['stream'],
            'level': 'INFO',
        },
    }
}

LANGUAGE_CODE = 'en-US'

TIME_ZONE = os.getenv("TIMEZONE", "UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = os.getenv("USE_TZ", "true") == "true"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]
AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
