import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')  # Put the actual key in .env

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['talentscout-2.onrender.com', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'corsheaders',
    'channels',

    # Your apps
    'users',
    'jobs',
    'employers',
    'messaging',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'users.middleware.EmployerOnlyMiddleware',
]

ROOT_URLCONF = 'talentscout.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'talentscout.wsgi.application'
ASGI_APPLICATION = 'talentscout.asgi.application'

# ✅ Use PostgreSQL in production; fallback to SQLite locally
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication
AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1

LOGIN_URL = '/users/employer-login/'
LOGIN_REDIRECT_URL = '/users/login-redirect/'
ACCOUNT_LOGIN_REDIRECT_URL = '/users/login-redirect/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/users/login-redirect/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*']
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_ADAPTER = 'users.adapter.CustomAccountAdapter'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    },
    'github': {
        'APP': {
            'client_id': config('GITHUB_CLIENT_ID'),
            'secret': config('GITHUB_CLIENT_SECRET'),
            'key': ''
        }
    }
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')  # Your email address
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  # Your email password or app password
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# Celery
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')

# Channels + Redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config("REDIS_URL", default="redis://127.0.0.1:6379")],
        },
    },
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {
        'jobs.views': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
