from django.conf import global_settings

"""
Django settings for drScratch project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATIC_URL = '/static/'

STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = '/static/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'An#l=@fMq$Dd=>h(iR&)IqM;/tL#M9&+K#ef^gy1vKdCSl+qdT'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True        

TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'app/templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            #'django.template.context_processors.debug',
            #'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            #'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
        ],
    },
},
]

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '100.91.170.113', 'www.drscratch.org']

INSTALLED_APPS = (
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drScratch.urls'

WSGI_APPLICATION = 'drScratch.wsgi.application'

# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'drscratchv3',
         'USER': 'root',
	 'PASSWORD':'Mysql.drscratch',
	 'HOST': 'localhost',
         'OPTIONS':{
                   'autocommit': True,
         }
    }
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = 'static'
MEDIA_URL = os.path.join(BASE_DIR,'static/img/')

# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

_ = lambda s: s

LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
    ('ca', _('Catalan')),
    ('gl', _('Galician')),
    ('pt', _('Portuguese')),
    ('el', _('Greek')),
    ('eu', _('Basque')),
    ('it', _('Italiano')),
    ('ru', _('Russian')),
)


SITE_ROOT = os.path.dirname(os.path.realpath(__name__))
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

#Send Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



