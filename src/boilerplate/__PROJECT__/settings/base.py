import os
from pathlib import Path

try:  # Optional dependency for DATABASE_URL parsing
    import dj_database_url  # type: ignore
except Exception:  # pragma: no cover
    dj_database_url = None  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me")

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes", "on")

def _split_env_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]

ALLOWED_HOSTS = _split_env_list(os.environ.get("DJANGO_ALLOWED_HOSTS")) or (["*"] if DEBUG else ["127.0.0.1", "localhost"])

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'drf_yasg',
]
USER_DEFINED_APPS = [
    '{{ app_name }}',
]

BUILT_IN_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


INSTALLED_APPS = BUILT_IN_APPS + THIRD_PARTY_APPS + USER_DEFINED_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "{{ project_name }}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

WSGI_APPLICATION = "{{ project_name }}.wsgi.application"

_database_url = os.environ.get("DATABASE_URL")
if _database_url and dj_database_url:
    DATABASES = {
        "default": dj_database_url.parse(_database_url, conn_max_age=int(os.environ.get("DB_CONN_MAX_AGE", "600")))
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get("DB_NAME", str(BASE_DIR / "db.sqlite3")),
        }
    }



LANGUAGE_CODE = os.environ.get("DJANGO_LANGUAGE_CODE", "en-us")
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = os.environ.get("DJANGO_STATIC_URL", "/static/")
STATIC_ROOT = Path(os.environ.get("DJANGO_STATIC_ROOT", str(BASE_DIR / "staticfiles")))

MEDIA_ROOT = Path(os.environ.get("DJANGO_MEDIA_ROOT", str(BASE_DIR / "media")))
MEDIA_URL = os.environ.get("DJANGO_MEDIA_URL", "/media/")


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

CORS_ALLOWED_ORIGINS = _split_env_list(os.environ.get("CORS_ALLOWED_ORIGINS"))
CORS_ALLOW_ALL_ORIGINS = (
    (os.environ.get("CORS_ALLOW_ALL_ORIGINS") or "").lower() in ("1", "true", "yes", "on")
    or (not CORS_ALLOWED_ORIGINS and DEBUG)
)
CORS_ALLOW_CREDENTIALS = (os.environ.get("CORS_ALLOW_CREDENTIALS", "True").lower() in ("1", "true", "yes", "on"))

CORS_ALLOWED_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CSRF_TRUSTED_ORIGINS = _split_env_list(os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
