from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AUTH_PASSWORD_VALIDATORS = []  # allow easy passwords only on local