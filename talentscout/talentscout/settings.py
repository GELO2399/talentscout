import os
from pathlib import Path
import django_heroku

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = ['*']

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

    'channels',

    # Your apps
    'users',
    'jobs',
    'employers',
    'messaging',
    'corsheaders',
]

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '1046805791858-ftfl1do52mque8ptplknfngkqoomj6h4.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    },
    'github': {
        'APP': {
            'client_id': '0v23liKtpdgufzFRIEJd',
            'secret': 'cc2cb3ec17d8e2a4b260178cd1718cc0f382ca90',
            'key': ''
        }
    }
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'users.middleware.EmployerOnlyMiddleware',


]
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'jobs.views': {  # Replace with your app's name
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

ROOT_URLCONF = 'talentscout.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

WSGI_APPLICATION = 'talentscout.wsgi.application'
ASGI_APPLICATION = 'talentscout.asgi.application'

# Database (use SQLite for simplicity)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CORS_ALLOWED_ORIGINS = [
    "https://your-app-name.onrender.com",
]
CORS_ALLOW_ALL_ORIGINS = True

# Authentication Backends for allauth
AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Redirect after login/logout
LOGIN_URL = '/users/employer-login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'iwasplayer1@gmail.com'
EMAIL_HOST_PASSWORD = 'ljmgrupnptxtddel'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Celery config
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# Channels config (Redis Layer)
CHANNEL_LAYERS = {
    
    'default': {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

# Allauth config
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# Channels and Redis Configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get("REDIS_URL", "redis://127.0.0.1:8000")],
        },
    },
}

# Activate Django-Heroku (for better Render compatibility)
django_heroku.settings(locals())
