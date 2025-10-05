import os
from pathlib import Path

import environ
from django.core.asgi import get_asgi_application

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    PRODUCTION=(bool, False),
)

environ.Env.read_env(str(BASE_DIR / ".env"))

is_production = env.bool("PRODUCTION", False)
settings_module = (
    "{{ project_name }}.settings.production"
    if is_production
    else "{{ project_name }}.settings.development"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_asgi_application()