from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from librehatti.config import _SENDER_EMAIL
from librehatti.config import _PASSWORD

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

ALLOWED_HOSTS = []

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = _SENDER_EMAIL
EMAIL_HOST_PASSWORD = _PASSWORD

TIME_ZONE = 'Asia/Kolkata'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCAL_URL = ''

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    '/path/to/LibreHatti/static',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SECRET_KEY = 'v5j3-ny)7zlk3wmqyg298#re3#8-v_v6+@9635h0-x9zak+8t*'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ROOT_URLCONF = 'librehatti.urls'

WSGI_APPLICATION = 'librehatti.wsgi.application'

TEMPLATE_DIRS = (
    'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'suit',
    'mptt',
    'django.contrib.admin',
    'librehatti.catalog',
    'useraccounts',
    'tinymce',
    'librehatti.prints',
    'librehatti.suspense',
    'librehatti.bills',
    'librehatti.reports',
    'librehatti.voucher',
    'librehatti.programmeletter',
)

SUIT_CONFIG = {
    'ADMIN_NAME': 'LibreHatti',
    'MENU_ICONS': {
        'sites': 'icon-leaf',
       'auth': 'icon-lock',
       'bills': 'icon-file',
     },
}


ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = 'admin:catalog'
LOGIN_URL = 'admin:login'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    },
}


AJAX_LOOKUP_CHANNELS = {
    'buyer': ('librehatti.catalog.lookups', 'BuyerLookup'),
    'staff': ('librehatti.programmeletter.stafflookups', 'StaffLookup'),
}
