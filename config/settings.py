"""
Django settings for the WIL Placement Management System.

All secrets and machine-specific values come from environment variables
(loaded from a local .env file in development). See .env.example.
Never commit your real .env file. (Phase 4, section 4.4.8)
"""
from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        raise ImproperlyConfigured(f"Set the {name} environment variable (see .env.example).")
    return value


def env_bool(name, default=False):
    return str(env(name, str(default))).strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    return [item.strip() for item in env(name, default).split(",") if item.strip()]


# --------------------------------------------------------------------------
# Core
# --------------------------------------------------------------------------
DEBUG = env_bool("DJANGO_DEBUG", False)
SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-insecure-key-change-me" if DEBUG else None, required=not DEBUG)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Project apps (one per module, so team members can work in parallel)
    "apps.core",
    "apps.accounts",
    "apps.organisations",
    "apps.placements",
    "apps.logbook",
    "apps.assessments",
    "apps.audit",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --------------------------------------------------------------------------
# Database: MySQL 8.0 + InnoDB + utf8mb4 (sections 4.4.6 and 4.5).
# Set DB_ENGINE=sqlite only for a quick local start without MySQL.
# --------------------------------------------------------------------------
DB_ENGINE = env("DB_ENGINE", "mysql").lower()

if DB_ENGINE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
elif DB_ENGINE == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env("DB_NAME", "wil_placement"),
            "USER": env("DB_USER", "wil_app"),
            "PASSWORD": env("DB_PASSWORD", ""),
            "HOST": env("DB_HOST", "127.0.0.1"),
            "PORT": env("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES', default_storage_engine=INNODB",
            },
            # Multi-step actions (placement approval, result capture) use transaction.atomic().
            "ATOMIC_REQUESTS": False,
        }
    }
else:
    raise ImproperlyConfigured("DB_ENGINE must be 'mysql' or 'sqlite'.")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------
# Authentication (custom user table `user`, email login, hashed passwords)
# --------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:dashboard"
LOGOUT_REDIRECT_URL = "accounts:login"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Sessions expire after 30 minutes of inactivity.
SESSION_COOKIE_AGE = int(env("SESSION_COOKIE_AGE", "1800"))
SESSION_SAVE_EVERY_REQUEST = True

# --------------------------------------------------------------------------
# Localisation
# --------------------------------------------------------------------------
LANGUAGE_CODE = "en-za"
FORMAT_MODULE_PATH = ["config.formats"]
TIME_ZONE = "Africa/Johannesburg"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# Static files and protected document storage (section 4.4.8)
# --------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Uploaded documents live OUTSIDE the web root and are only served through
# the permission-checked download view in apps.placements. There is no
# public MEDIA_URL route.
MEDIA_ROOT = Path(env("DOCUMENT_STORAGE_PATH", str(BASE_DIR / "protected_media")))
MEDIA_URL = "/protected/"  # never served directly

DOCUMENT_MAX_UPLOAD_MB = int(env("DOCUMENT_MAX_UPLOAD_MB", "10"))
DOCUMENT_ALLOWED_EXTENSIONS = ["pdf", "docx", "jpg", "jpeg", "png"]
DATA_UPLOAD_MAX_MEMORY_SIZE = DOCUMENT_MAX_UPLOAD_MB * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 2_621_440

# --------------------------------------------------------------------------
# Email (notifications). Console backend prints emails in development.
# --------------------------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", "")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "WIL Placement System <no-reply@localhost>")

# --------------------------------------------------------------------------
# Production hardening (section 4.4.9): active automatically when DEBUG is off.
# --------------------------------------------------------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(env("DJANGO_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL", "INFO")},
    # 403/404 responses are normal (e.g. permission checks); only log real errors.
    "loggers": {"django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False}},
}
