
from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
from django.utils.translation import gettext_lazy as _


load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "unfold",  
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # logo após SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = 'ecotrip_admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecotrip_admin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DATABASE_NAME'),
#         'USER': os.getenv('DATABASE_USER'),
#         'PASSWORD': os.getenv('DATABASE_PASSWORD'),
#         'HOST': os.getenv('DATABASE_HOST'),
#         'PORT': os.getenv('DATABASE_PORT'),
#     }
# }
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),  # a URL fornecida pelo Render
        conn_max_age=600,                   # keep-alive de conexões (opcional)
        ssl_require=False                    # se você precisa de SSL
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("pt", _("Português")),
    ("es", _("Español")),
    ("fr", _("Français")),
    ("en", _("English")),
]

USE_I18N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

UNFOLD = {
    "SITE_TITLE": "Ecotrip",         # título na aba do navegador
    "SITE_HEADER": "Dashboard Admin",   # cabeçalho
    "SITE_ICON": None,                  # favicon (podes colocar um path)
    "SITE_LOGO": None,                  # logotipo no header/sidebar
    "SITE_SYMBOL": "🚀",                # emoji de fallback
    #"DASHBOARD_CALLBACK": "app.dashboard.get_widgets",  # função para dashboard
    "SHOW_HISTORY": True,               # mostra histórico no changelist
    "SHOW_VIEW_ON_SITE": True,          # mostra "ver no site"
    "DARK_MODE": True,                  # força dark mode
    "SHOW_LANGUAGES": True,
}
