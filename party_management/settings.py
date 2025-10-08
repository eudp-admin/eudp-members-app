import os
from pathlib import Path
import dj_database_url
from environ import Env

# --- Environment Setup ---
BASE_DIR = Path(__file__).resolve().parent.parent
env = Env()

# .env ፋይል በአካባቢው (Local) ላይ ካለ ብቻ እንዲነበብ ማድረግ።
# ይህ Render ላይ ስህተት እንዳይፈጥር ይከላከላል።
if os.path.exists(os.path.join(BASE_DIR.parent, '.env')):
    Env.read_env(os.path.join(BASE_DIR.parent, '.env')) 
elif os.path.exists(os.path.join(BASE_DIR, '.env')):
    Env.read_env(os.path.join(BASE_DIR, '.env')) 


SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False) 

# --- Host Configuration ---
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME') 
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    
    'cloudinary',
    'cloudinary_storage', 
    
    'crispy_forms',
    'crispy_bootstrap5',
    'members.apps.MembersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'party_management.urls'
WSGI_APPLICATION = 'party_management.wsgi.application'

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

# --- Database Configuration ---
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{os.path.join(BASE_DIR, "db.sqlite3")}',
        conn_max_age=600,
        ssl_require=not DEBUG 
    )
}

# ... (AUTH_PASSWORD_VALIDATORS, LOGIN_URL, LANGUAGE_CODE, ወዘተ...)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'landing_page'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# party_management/settings.py

# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

# --- Static Files (served by WhiteNoise) ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- Media Files (Conditional: Cloudinary for Production, Local for Development) ---
MEDIA_URL = '/media/'

# Get Cloudinary credentials from environment variables using django-environ
CLOUDINARY_CLOUD_NAME = env('CLOUDINARY_CLOUD_NAME', default=None)
CLOUDINARY_API_KEY = env('CLOUDINARY_API_KEY', default=None)
CLOUDINARY_API_SECRET = env('CLOUDINARY_API_SECRET', default=None)

# Check if all Cloudinary credentials are provided
if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    # PRODUCTION SETTINGS (using Cloudinary)
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
        'API_KEY': CLOUDINARY_API_KEY,
        'API_SECRET': CLOUDINARY_API_SECRET,
    }
    print("INFO: Cloudinary credentials found. Using Cloudinary for media.")
else:
    # DEVELOPMENT SETTINGS (using local file system)
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    os.makedirs(MEDIA_ROOT, exist_ok=True)
    print("INFO: Cloudinary credentials not found. Using local file storage for media.")