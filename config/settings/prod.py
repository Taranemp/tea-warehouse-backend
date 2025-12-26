from .base import *
import os
from decouple import Config, RepositoryEnv

ENV_PATH = "/home1/salidevl/teatracer-api.salidevlab.ir/backend/.env"

if os.path.exists(ENV_PATH):
    config = Config(repository=RepositoryEnv(ENV_PATH))


DEBUG = False

# --- Security ---
SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --- Database ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

# --- Static & Media ---
STATIC_URL = "/static/"
STATIC_ROOT = "/home1/salidevl/teatracer-api.salidevlab.ir/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/home1/salidevl/teatracer-api.salidevlab.ir/media"

DEBUG_PROPAGATE_EXCEPTIONS = False

GITHUB_WEBHOOK_SECRET = config("GITHUB_WEBHOOK_SECRET")
