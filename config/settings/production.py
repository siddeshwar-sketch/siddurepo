from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']
# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Production database (Postgres/MySQL)
# Fallback to SQLite during build if DATABASE_URL is missing
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

# For static files in production, use Whitenoise or Nginx.
# We'll rely on Nginx in docker-compose.
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Use Whitenoise for efficient static file serving
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# EMAIL CONFIGURATION (Gmail Recommended)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default=EMAIL_HOST)
EMAIL_PORT = env.int('EMAIL_PORT', default=EMAIL_PORT)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=EMAIL_USE_TLS)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default=EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default=EMAIL_HOST_PASSWORD)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
}
