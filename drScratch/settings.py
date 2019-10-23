import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = '/static/'


SECRET_KEY = os.environ.get('DRSCRATCH_SECRET_KEY', 'not-secret-key')

DEBUG = os.environ.get('DRSCRATCH_DEBUG', False)

TEMPLATE_DEBUG = True

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'app/templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
        ],
    },
}]


# ALLOWED_HOSTS = os.environ.get('DRSCRATCH_ALLOWED_HOSTS').split(",")
ALLOWED_HOSTS = os.environ.get('DRSCRATCH_ALLOWED_HOSTS').split(",")

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
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drScratch.urls'

WSGI_APPLICATION = 'drScratch.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DRSCRATCH_SQLENGINE'),
        'NAME': os.environ.get('DRSCRATCH_DATABASE_NAME'),
        'USER': os.environ.get('DRSCRATCH_DATABASE_USER'),
        'PASSWORD': os.environ.get('DRSCRATCH_DATABASE_PASSWORD'),
        'HOST': os.environ.get('DRSCRATCH_DATABASE_HOST'),
        'PORT': os.environ.get('DRSCRATCH_DATABASE_PORT'),
        'OPTIONS': {
               'autocommit': True,
        }
    }
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

MEDIA_ROOT = 'static'
MEDIA_URL = os.path.join(BASE_DIR, 'static/img/')

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

# Send Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'angelavargasalba@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
