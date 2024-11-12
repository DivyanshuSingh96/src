from pathlib import Path
from decouple import config as env_config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_config("DJANGO_DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = [".vercel.app"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "imageUpload",
    "imageViewer",
    "key_management",

    "rest_framework",
    "corsheaders",
    "tailwind",
    "theme",
    "django_browser_reload",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
}

TAILWIND_APP_NAME = "theme"

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

ROOT_URLCONF = 'cloud_storage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "theme/templates"],
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

WSGI_APPLICATION = 'cloud_storage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ]
# }

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#         # Other authentication classes can be added here
#     ),
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug2.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory for collected static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'theme/static'),  # Directory where your static files are located
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CLOUDFLARE_R2_BUCKET=env_config("CLOUDFLARE_R2_BUCKET")
CLOUDFLARE_R2_ACCESS_KEY=env_config("CLOUDFLARE_R2_ACCESS_KEY")
CLOUDFLARE_R2_SECRET_KEY=env_config("CLOUDFLARE_R2_SECRET_KEY")
CLOUDFLARE_R2_BUCKET_ENDPOINT=env_config("CLOUDFLARE_R2_BUCKET_ENDPOINT")

CLOUDFLARE_R2_CONFIG_OPTIONS = {
    "bucket_name": CLOUDFLARE_R2_BUCKET,
    "access_key": CLOUDFLARE_R2_ACCESS_KEY,
    "secret_key": CLOUDFLARE_R2_SECRET_KEY,
    "endpoint_url": CLOUDFLARE_R2_BUCKET_ENDPOINT,
    "default_acl": "public-read", # acl -> access control private
    "signature_version": "s3v4",
}

CLOUDFLARE_ACCOUNT_ID=env_config("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_KEY=env_config("CLOUDFLARE_API_KEY")
CLOUDFLARE_ACCOUNT_HASH=env_config("CLOUDFLARE_ACCOUNT_HASH")
CLOUDFLARE_IMAGES_DOMAIN=env_config("CLOUDFLARE_IMAGES_DOMAIN")
CLOUDFLARE_EMAIL=env_config("CLOUDFLARE_EMAIL")

# Django staticfiles config for storages

STORAGES = {
    "default": {
        "BACKEND": "helpers.cloudflare.storages.MediaFileStorage", # django-storage[s3]
        "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS
    }, # default -> user/ image/ file fields uploads
    "staticfiles": {
        "BACKEND": "helpers.cloudflare.storages.StaticFileStorage", # django-storage[s3]
        "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS
    }, # staticfiles
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_WHITELIST = [
    "http://localhost:5173",
]

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]