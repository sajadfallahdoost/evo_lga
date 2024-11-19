from datetime import timedelta
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-j3&ursom8adj6qoft(v8f)5$0yc)dw*bia^5k&89ow!3*n=$@#'

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "192.168.100.234", "localhost", "192.168.100.254"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'rest_framework',
    'drf_yasg',
    'painless',
    'product',
    'basket',
    'discount',
    'corsheaders',
    "azbankgateways",
    'payments',
    # 'support',
    'logistic',
    'services',
    'services.otp',
    # 'services.payment',
    # "services.payment.payment_sep",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kernel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'kernel.wsgi.application'


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "hamrahcel",
        "USER": "hamrahcel_user",
        "PASSWORD": "Sf35741381@",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "TEST": {"NAME": "hamrahcell_test"},
    },
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


AZ_IRANIAN_BANK_GATEWAYS = {
    "GATEWAYS": {
        # "BMI": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        #     "TERMINAL_CODE": "<YOUR TERMINAL CODE>",
        #     "SECRET_KEY": "<YOUR SECRET CODE>",
        # },
        # "SEP": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        #     "TERMINAL_CODE": "<YOUR TERMINAL CODE>",
        # },
        # "IDPAY": {
        #     "MERCHANT_CODE": "6a7f99eb-7c20-4412-a972-6dfb7cd253a4",
        #     "METHOD": "POST",  # GET or POST
        #     "X_SANDBOX": 1,  # 0 disable, 1 active
        # },
        # "ZARINPAL": {
        #     "MERCHANT_CODE": "6a7f99eb-7c20-4412-a972-6dfb7cd253a4",
        #     "SANDBOX": 1,  # 0 disable, 1 active
        # },
        # "ZIBAL": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        # },
        # "BAHAMTA": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        # },
        "MELLAT": {
            "TERMINAL_CODE": "6189178",
            "USERNAME": "HAMRAHCEL777",
            "PASSWORD": "43575199",
        },
        # "PAYV1": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        #     "X_SANDBOX": 1,  # 0 disable, 1 active
        # },
    },
    "IS_SAMPLE_FORM_ENABLE": True,  # اختیاری و پیش فرض غیر فعال است
    "DEFAULT": "MELLAT",
    "CURRENCY": "IRR",  # اختیاری
    "TRACKING_CODE_QUERY_PARAM": "tc",  # اختیاری
    "TRACKING_CODE_LENGTH": 16,  # اختیاری
    "SETTING_VALUE_READER_CLASS": "azbankgateways.readers.DefaultReader",  # اختیاری
    "BANK_PRIORITIES": ["MELLAT"],
    #     "BMI",
    #     "SEP",
    #     # and so on ...
    # ],  # اختیاری
    "IS_SAFE_GET_GATEWAY_PAYMENT": False,  # اختیاری، بهتر است True بزارید.
    "CUSTOM_APP": None,  # اختیاری
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Optionally, set the default timeout for keys
CACHE_TTL = 180  # 2 minutes

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'amieseansi@gmail.com'
EMAIL_HOST_PASSWORD = 'qblg uvce gdzg frzc'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}


AUTH_USER_MODEL = 'account.User'

MERCHANT = "00000000-0000-0000-0000-000000000000"

SANDBOX = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite's default development server
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:7000",
    "http://192.168.100.236:7000",
    "http://91.198.77.38:8000",
    "http://91.198.77.38",
    "https://91.198.77.38",
    "https://91.220.113.138",
]

# For development only - remove in production
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:7000",
    "http://192.168.100.236:7000",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://91.198.77.38:8000",
    "http://91.198.77.38",
    "https://91.198.77.38",
    "https://91.220.113.138",
]
