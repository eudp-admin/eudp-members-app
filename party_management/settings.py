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


# --- Static Files (WhiteNoise) ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Media Files (Cloudinary) ---
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage' 

# 🔑 ወሳኝ ጊዜያዊ ማስተካከያ: ቁልፎችን በቀጥታ በኮድ ማስገባት (ለሙከራ ብቻ!)
# ይህንን ካረጋገጡ በኋላ ወዲያውኑ ወደ env() መመለስ አለብዎት!
CLOUDINARY_STORAGE = {
    # እባክዎ "YOUR_REAL_CLOUD_NAME" በሚለው ቦታ ትክክለኛውን Cloud Name ያስገቡ
    'CLOUD_NAME': 'dfxa9kcwo',          
    # እባክዎ "YOUR_REAL_API_KEY" በሚለው ቦታ ትክክለኛውን API Key ያስገቡ
    'API_KEY': '423646351335998',             
    # እባክዎ "YOUR_REAL_API_SECRET" በሚለው ቦታ ትክክለኛውን API Secret ያስገቡ
    'API_SECRET': 'OcevBOwyVXCC9U878V176LVLysc',       
}