"""
Django settings for quickbooks_interface project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o#9*+gf76w_av@p-p(mnfh1kbo!c)mzo-!5&3vm)i!=iek-ekb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#     'mesika_plugins.sms_notifications',
#     'mesika_plugins.email_notifications',
#     'mesika_plugins.im_notifications',
    'quickbooks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quickbooks_interface.urls'

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

WSGI_APPLICATION = 'quickbooks_interface.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'quickbooks',
       'USER': 'banqphast',
       'PASSWORD': 'Gq6@FQx7s098',
       'HOST': 'localhost',
       'PORT': '65320',
   }
}



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CELERY_TASK_ALWAYS_EAGER = False
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TASK_CREATE_MISSING_QUEUE = True
CELERY_TASK_QUEUES = {
    'agency_banking': {
        'exchange': 'agency_banking',
        'routing_key': 'agency_banking',
    },
}

CELERY_TASK_ROUTES = {
    # SERVICES
    'agency_banking': {
        'queue': 'agency_banking',
        'exchange': 'agency_banking',
        'routing_key': 'agency_banking', },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]

# OAuth specific variables
DISCOVERY_DOCUMENT = 'https://developer.api.intuit.com/.well-known/openid_sandbox_configuration/'
#CLIENT_ID = 'AB2Qh0of7tiukfJYEZEtXJAuUm1haum0THg0LhorkAwClEzrkU'
CLIENT_ID = 'ABYaZFQZdVsloRzdqpS4Ajjp4KcUkdBRc6i34HYygubZ9xJ6ic'
#CLIENT_SECRET = 'C73zLYGYO6lcEMhP6BRl2W8fS3Mif1pCoO9nKmPW'
CLIENT_SECRET = 'gkGoIuLWwcCKct3p0GguLcdhT2INOU01Bp9QI8Qc'
#REDIRECT_URI = 'http://localhost:7000/quickbooks-core-interface/quickbooks/complete_connection/'
REDIRECT_URI = 'https://banqphast.mesika.org:4443/banqphast-corporate/accounts/erp/sign-in/response'
#REDIRECT_URI = 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl'
ACCOUNTING_SCOPE = 'com.intuit.quickbooks.accounting'
OPENID_SCOPES = ['openid', 'profile', 'email', 'phone', 'address']
GET_APP_SCOPES = ['com.intuit.quickbooks.accounting', 'openid', 'profile', 'email', 'phone', 'address', 'invoice', 'payment']
SANDBOX_QBO_BASEURL = 'https://sandbox-quickbooks.api.intuit.com'
SANDBOX_PROFILE_URL = 'https://sandbox-accounts.platform.intuit.com/v1/openid_connect/userinfo'
ID_TOKEN_ISSUER = 'https://oauth.platform.intuit.com/op/v1'

INVOICE = "https://quickbooks.api.intuit.com/v3/company/12345678/invoice"

REVOKE_TOKEN = "https://developer.api.intuit.com/v2/oauth2/tokens/revoke"
BEARER_TOKEN = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
JWT_KEY = "https://oauth.platform.intuit.com/op/v1/jwks"
CONNECT_QUICKBOOKS = "https://appcenter.intuit.com/connect/oauth2"

INVOICE_PAYMENT_START = "https://sandbox-quickbooks.api.intuit.com/v3/company/"
INVOICE_PAYMENT_END = "/query?query=select%20*%20from%20Payment%20Where%20Metadata.LastUpdatedTime%3E%272015-01-16%27%20OrderBy%20Metadata.LastUpdatedTime&minorversion=54"
REFRESH_TOKEN =  "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

CUSTOMER_ENDPOINT = "https://sandbox-quickbooks.api.intuit.com/v3/company/"
