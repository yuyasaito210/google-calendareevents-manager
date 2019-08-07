"""
Django settings for google_calendar_events_manager project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import psycopg2

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3@gs_f8jg+!$-5e7&9jtj-%0=ykxa2i*it=@o%z-*%)oa6b=(b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'ea3f60cd.ngrok.io',
    os.environ.get('SERVER_HOST', 'gceventmanager.herokuapp.com')
]


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'import_export',
    'nested_admin'
]

LOCAL_APPS = [
    'senders',
    'accounts',
    'events',
    'event_receivers'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'gcevents'),
        'USER': os.environ.get('DB_USER_NAME', 'postgres'),
        'PASSWORD': os.environ.get('DB_USER_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    },
    'OPTIONS': {
        'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
IMPORT_EXPORT_USE_TRANSACTIONS = True
TIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%Y/%m/%d %H:%M:%S',     # '2006/10/25 14:30:59'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
]
GOOGLE_CALENDAR_API_CLIENT_ID = os.environ.get(
    'GOOGLE_CALENDAR_API_CLIENT_ID', 
    '495916345885-aglgq6s3prr601o62i693tqjrhfkk8q5.apps.googleusercontent.com'
)
GOOGLE_CALENDAR_API_CLIENT_SECRET = os.environ.get(
    'GOOGLE_CALENDAR_API_CLIENT_SECRET', 
    '0IYV7UcwuRmmTIdNN5QyXcTa'
)
GOOGLE_CALENDAR_API_APP_NAME = os.environ.get(
    'GOOGLE_CALENDAR_API_APP_NAME', 
    'GccEnventManagerAPI'
)
GOOGLE_CALENDAR_API_REDIRECT_URI = os.environ.get(
    'GOOGLE_CALENDAR_API_REDIRECT_URI', 
    'https://ea3f60cd.ngrok.io'
)

HTTPS_PROXY = os.environ.get(
    'https_proxy', 
    'https://ninjadev:123qweasd@gate.smartproxy.com:7000'
)
HTTP_PROXY = os.environ.get(
    'http_proxy', 
    'https://ninjadev:123qweasd@gate.smartproxy.com:7000'
)

SMART_PROXY_HTTPS_URL =  os.environ.get(
    'SMART_PROXY_HTTPS_URL', 
    'https://ninjadev:123qweasd@gate.smartproxy.com:7000'
)
SMART_PROXY_HTTP_URL = os.environ.get(
    'SMART_PROXY_HTTP_URL', 
    'http://ninjadev:123qweasd@gate.smartproxy.com:7000'
)
SMART_PROXY_ADDRESS = os.environ.get(
    'gate.smartproxy.com', 
    7000
)
SMART_PROXY_PORT = os.environ.get(
    'SMART_PROXY_PORT', 
    7000
)
SMART_PROXY_USER_NAME = os.environ.get(
    'SMART_PROXY_USER_NAME', 
    'sp45159786'
    # 'ninjadev'
)
SMART_PROXY_PASSWORD = os.environ.get(
    'SMART_PROXY_PASSWORD', 
    'Y**UY6M9Bbj'
    # '123qweasd'
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'request_token': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")