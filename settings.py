"""
Django settings for uberchallenge project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k&+fcs5#9-cc@f_b%(g7s!$f7e^xso$!kl*fo&8^gzg-omqrj='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (

	os.path.join(os.path.dirname(__file__), 'templates'),
	os.path.join(os.path.dirname(__file__), 'departure/templates'),

)

REST_FRAMEWORK = {
	'DEFAULT_PARSER_CLASSES': {
		'rest_framework.parsers.XMLParser',
	}
}

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'easy_maps',
    'departure',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'uberchallenge.urls'

WSGI_APPLICATION = 'uberchallenge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
		'NAME': 'geodeparture',  # Name of your spatial database
        'USER': 'geo',   # Database user 
        'PASSWORD' : '1234',
        'HOST': 'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Geolocation file locations
GEOIP_PATH = BASE_DIR + '/geoIP'
GEOS_LIBRARY_PATH = '/usr/local/lib/libgeos_c.so'
GDAL_LIBRARY_PATH = '/usr/local/lib/libgdal.so'
