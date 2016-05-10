# from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from librehatti.config import _SENDER_EMAIL
from librehatti.config import _PASSWORD

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'v5j3-ny)7zlk3wmqyg298#re3#8-v_v6+@9635h0-x9zak+8t*'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    'mptt',
    'ajax_select',
    'tinymce',
    'useraccounts',
    'librehatti.catalog',
    'librehatti.prints',
    'librehatti.suspense',
    'librehatti.bills',
    'librehatti.reports',
    'librehatti.voucher',
    'librehatti.programmeletter',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'librehatti.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'librehatti.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'db_username',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/librehatti/static/'

STATICFILES_DIRS = [
os.path.join(BASE_DIR, "static"),
]

AJAX_LOOKUP_CHANNELS = {
    'buyer': ('librehatti.catalog.lookups', 'BuyerLookup'),
    'staff': ('librehatti.programmeletter.stafflookups', 'StaffLookup'),
}

SUIT_CONFIG = {
    'ADMIN_NAME': 'LibreHatti',
    'MENU_ICONS': {
        'sites': 'icon-leaf',
       'auth': 'icon-lock',
       'bills': 'icon-file',
     },
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = _SENDER_EMAIL
EMAIL_HOST_PASSWORD = _PASSWORD

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = 'admin:catalog'
LOGIN_URL = 'admin:login'

# SITE_ID = 1

# TEMPLATE_CONTEXT_PROCESSORS = TCP + (
#     'django.core.context_processors.request',
# )

# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# 
# )

# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )

# TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         }
#     },
# }



