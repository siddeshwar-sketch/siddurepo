from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Use SQLite for local development by default, unless overridden by DATABASE_URL
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

# Email Configuration (Reads from .env)
# These are already defined in base.py but we allow overrides here
EMAIL_BACKEND = env('EMAIL_BACKEND', default=EMAIL_BACKEND)
EMAIL_HOST = env('EMAIL_HOST', default=EMAIL_HOST)
EMAIL_PORT = env('EMAIL_PORT', default=EMAIL_PORT, cast=int)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=EMAIL_USE_TLS, cast=bool)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default=EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default=EMAIL_HOST_PASSWORD)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

