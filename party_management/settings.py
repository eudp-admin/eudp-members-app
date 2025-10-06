"""
Django settings for party_management project.
"""
import os
from pathlib import Path
import dj_database_url

# ==============================================================================
# CORE SETTINGS & ENVIRONMENT VARIABLES
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Use .env file for local development
# In production (Render), these will be set in the environment.
from environ import Env
env = Env()
Env.read_env(os.path.join(BASE_DIR, '.env'))

# Secret Key (with a fallback for local development)
SECRET_KEY = env('SECRET_KEY', default='django-insecure-fallback-key-for-local-dev')

# Debug Mode (reads 'True'/'False' from env as boolean)
DEBUG = env.bool('DEBUG', default=True) # Default to True for safety in local dev

# Allowed Hosts & Security
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = env('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    # Add local hosts for development
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])

CSRF_TRUSTED_ORIGINS = [f'https://{RENDER_EXTERNAL_HOSTNAME}'] if RENDER_EXTERNAL_HOSTNAME else []

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'whitenoise.runserver_nostatic', # Must come after cloudinary_storage
    'django.contrib.staticfiles',
    'cloudinary',

    # Third-party Apps
    'crispy_forms',
    'crispy_bootstrap5',
    'qrcode',

    # Local Apps
    'members.apps.MembersConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Correctly placed
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'party_management.urls'
WSGI_APPLICATION = 'party_management.wsgi.application'

# ==============================================================================
# TEMPLATES & CRISPY FORMS
# ==============================================================================
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
            ],
        },
    },
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ==============================================================================
# DATABASE
# ==============================================================================
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default=f'sqlite:///{os.path.join(BASE_DIR, "db.sqlite3")}'),
        conn_max_age=600,
        ssl_require=not DEBUG # Use SSL in production, not in local dev
    )
}

# ==============================================================================
# AUTHENTICATION & PASSWORD VALIDATION
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'landing_page'

# ==============================================================================
# INTERNATIONALIZATION (I18N)
# ==============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

# --- Static Files ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if not DEBUG: # Use WhiteNoise storage only in production
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Media Files (Cloudinary / Local) ---
MEDIA_URL = '/media/'
CLOUDINARY_CLOUD_NAME = env('CLOUDINARY_CLOUD_NAME', default=None)
CLOUDINARY_API_KEY = env('CLOUDINARY_API_KEY', default=None)
CLOUDINARY_API_SECRET = env('CLOUDINARY_API_SECRET', default=None)

if CLOUDINARY_CLOUD_NAME:
    # PRODUCTION (Cloudinary)
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # DEVELOPMENT (Local)
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    os.makedirs(MEDIA_ROOT, exist_ok=True)