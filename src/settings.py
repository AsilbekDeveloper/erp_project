"""
src/settings.py
Django 5.2 – ERP project
"""

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

# ──────────── Load env ────────────
load_dotenv()

# ──────────── Base dir ────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────── Security ────────────
SECRET_KEY = "django-insecure-y+4pv@o-_@=6pwrx0=2_p^n@kh3(a1fxf7*rgayd6$(_46qd$="
DEBUG = True
# DEBUG = os.getenv("DEBUG", False)
ALLOWED_HOSTS = ["*"]

# ──────────── Installed apps ────────────
DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]
LOCAL_APPS = [
    "apps.core",
    "apps.dashboard",
    "apps.inventory",
    "apps.sales",
    "apps.expenses",
    "apps.reports",
    "apps.users",
    "widget_tweaks",
]
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

# ──────────── Middleware ────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "src.urls"

# ──────────── Templates ────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # loyihaviy ‘templates/’ papkasi
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "src.wsgi.application"

# ──────────── Database ────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# Postgres misoli:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "erp_db",
#         "USER": "erp_user",
#         "PASSWORD": "strong_pass",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

# ──────────── Auth  ────────────
AUTH_USER_MODEL = "users.User"  # custom user
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ──────────── i18n / tz ────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

# ──────────── Static & Media ────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # prod: collectstatic

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ──────────── Default PK ────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ──────────── Email (dev console) ────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# Prod’da SMTP sozlang

# ──────────── Session (optional) ────────────
SESSION_COOKIE_AGE = 60 * 60 * 24  # 1 kun
SESSION_SAVE_EVERY_REQUEST = True

# ──────────── Logging (minimal) ────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
