#!/usr/bin/env python
import os
import sys


def main():
    import environ
    from pathlib import Path

    base_dir = Path(__file__).resolve().parent

    env = environ.Env(
        PRODUCTION=(bool, False),
    )

    environ.Env.read_env(str(base_dir / ".env"))

    is_production = env.bool("PRODUCTION", False)
    settings_module = (
        "{{ project_name }}.settings.production"
        if is_production
        else "{{ project_name }}.settings.development"
    )
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
