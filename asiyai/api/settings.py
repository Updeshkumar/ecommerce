
import os
from dotenv import dotenv_values
config = dotenv_values(".env")
from corsheaders.defaults import default_headers
from pathlib import Path
import dj_database_url
#print(config.get('DATABASE_NAME'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + ('zone-offset',)


# Application definition

INSTALLED_APPS = [
    'adminlte3',
    'adminlte3_theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'user',
    'django_filters',
    'rosetta',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#DATABASES = {'default': dj_database_url.parse('mysql://minzor:minzor@123@mysql.gb.stackcp.com:55151/minzordev-31323549a3', conn_max_age=600)}

DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': config.get('DATABASE_NAME'),
    'USER': config.get('DATABASE_USER'),
    'PASSWORD': config.get('DATABASE_PASSWORD'),
    'HOST': config.get('DATABASE_HOST'),
    'PORT': config.get('DATABASE_PORT'),     
    'OPTIONS': {'charset': 'utf8mb4'},
    },
    'OPTIONS': {
     "init_command": "SET foreign_key_checks = 0;",
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'user')
MEDIA_URL = "/"
##### change static root up today ######################
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
##### change static root rahul shadiram today ######################
#STATIC_ROOT = "/home/breuh1vj9ohc/public_html/api.shadiram.in/static"
image_uploadPath =os.path.join(BASE_DIR, 'user/static/Uploaded/UserProfiles/')
doc_uploadPath =os.path.join(BASE_DIR, 'user/static/Uploaded/UserDocs/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR,"static"
]


from django.utils.translation import gettext_lazy as _

LANGUAGES = [
('en', _('English')),
('hi', _('hindi')),
('kn', _('Kannada')),
('mr', _('Marathi')),
('tr', _('Turkish')),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR,'locale'),
)