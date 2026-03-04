"""
Django settings for restaurant_project project.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-+x5!v4i%^8&j5@9n!q2w3e4r5t6y7u8i9o0p1q2w3e4r5t6y7u8i9o0p1')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Настройка разрешенных хостов
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.vercel.app', '.now.sh']

# Render.com hostname
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'menu',
    'orders',
    'tables',
    'accounts',
    'reports',
    'booking',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Для статических файлов
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurant_project.urls'

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

WSGI_APPLICATION = 'restaurant_project.wsgi.application'

# Database
# Настройка для Render (PostgreSQL) и локально (SQLite)
if 'RENDER' in os.environ:
    # На Render используем PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Локально используем SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# PWA Configuration
PWA_APP_NAME = 'АИС Общепит'
PWA_APP_DESCRIPTION = "Автоматизация ресторана"
PWA_APP_THEME_COLOR = '#0d6efd'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {'src': '/static/icons/icon-72x72.png', 'sizes': '72x72'},
    {'src': '/static/icons/icon-96x96.png', 'sizes': '96x96'},
    {'src': '/static/icons/icon-128x128.png', 'sizes': '128x128'},
    {'src': '/static/icons/icon-144x144.png', 'sizes': '144x144'},
    {'src': '/static/icons/icon-152x152.png', 'sizes': '152x152'},
    {'src': '/static/icons/icon-192x192.png', 'sizes': '192x192'},
    {'src': '/static/icons/icon-384x384.png', 'sizes': '384x384'},
    {'src': '/static/icons/icon-512x512.png', 'sizes': '512x512'}
]
PWA_APP_ICONS_APPLE = [
    {'src': '/static/icons/icon-152x152.png', 'sizes': '152x152'}
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'ru-RU'
PWA_APP_SHORTCUTS = [
    {'name': 'Главная', 'url': '/', 'description': 'На главную'},
    {'name': 'Меню', 'url': '/menu/', 'description': 'Посмотреть меню'},
    {'name': 'Бронирование', 'url': '/booking/', 'description': 'Забронировать стол'}
]

# Локальные настройки для разработки
try:
    from .local_settings import *
except ImportError:
    pass