"""
File management utilities for Django project setup.
Handles creation and modification of project files.
"""

import os
import subprocess

try:
    from .console import UIFormatter
except ImportError:
    from console import UIFormatter


class FileManager:
    """Manages file operations for Django project setup."""

    def __init__(self, project_root: str, project_name: str, app_name: str):
        self.project_root = project_root
        self.project_name = project_name
        self.app_name = app_name
        self.project_configs = os.path.join(project_root, project_name)
        self.settings_folder = os.path.join(self.project_configs, "settings")
        self.settings_file = os.path.join(self.project_configs, "settings.py")

    def create_gitignore(self) -> bool:
        """Create .gitignore file with Django-specific patterns."""
        try:
            os.chdir(self.project_root)

            gitignore_content = [
                "*.pyc",
                "__pycache__/",
                "*.sqlite3",
                "db.sqlite3",
                "env",
                ".env",
                ".vscode",
                ".idea",
                "*.DS_Store",
                "media/",
                "staticfiles/",
                "logs/",
                "*.log",
                ".coverage",
                "htmlcov/",
                ".pytest_cache/",
                "node_modules/",
                "venv/",
                ".venv/",
            ]

            with open(".gitignore", "w") as file:
                file.write("\n".join(gitignore_content) + "\n")

            UIFormatter.print_success("Created .gitignore file")
            return True
        except Exception as e:
            UIFormatter.print_error(f"Failed to create .gitignore: {str(e)}")
            return False

    def create_requirements(self) -> bool:
        """Create requirements.txt with Django dependencies."""
        try:
            os.chdir(self.project_root)

            requirements = [
                "Django>=5.2.7",
                "python-dotenv>=1.1.1",
                "django-jazzmin>=3.0.1",
                "djangorestframework>=3.16.1",
                "djangorestframework_simplejwt>=5.5.1",
                "drf-spectacular>=0.28.0",
                "django-cors-headers>=4.9.0",
                "whitenoise>=6.8.2",
                "psycopg2-binary>=2.9.9",  # For PostgreSQL support
                "gunicorn>=21.2.0",  # For production deployment
            ]

            with open("requirements.txt", "w") as file:
                file.write("\n".join(requirements) + "\n")

            UIFormatter.print_success(
                "Created requirements.txt with Django dependencies"
            )
            return True
        except Exception as e:
            UIFormatter.print_error(f"Failed to create requirements.txt: {str(e)}")
            return False

    def create_readme(self) -> bool:
        """Create basic README.md file."""
        try:
            os.chdir(self.project_root)

            readme_content = f"""# {self.project_name}

A Django project created with django-setup.

## Features

- Modern project structure with environment-specific settings
- Pre-configured REST API with JWT authentication
- Essential dependencies and utilities
- Production-ready configuration

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables in `.env` file

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Start development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
{self.project_name}/
├── {self.project_name}/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── {self.app_name}/
├── manage.py
├── requirements.txt
├── .env.sample
└── README.md
```

## API Documentation

When running in development mode, API documentation is available at:
- Swagger UI: http://localhost:8000/docs/
- Schema: http://localhost:8000/schema/
"""

            with open("README.md", "w") as file:
                file.write(readme_content)

            UIFormatter.print_success("Created README.md file")
            return True
        except Exception as e:
            UIFormatter.print_error(f"Failed to create README.md: {str(e)}")
            return False

    def create_env_file(self) -> bool:
        """Create .env.sample file with environment variables."""
        try:
            os.chdir(self.project_root)

            env_content = f"""# Django settings
DJANGO_SETTINGS_MODULE={self.project_name}.settings.development
SECRET_KEY=django-insecure-gs(+tg3%34((t$k(+6s5&n7b5@u)ruosu^&up00tr8ibuvml)a
ALLOWED_HOSTS=api.your-domain.com,www.your-domain.com

# Database
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Email settings
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USE_TLS=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

"""

            with open(".env.sample", "w") as file:
                file.write(env_content)

            UIFormatter.print_success("Created .env.sample file")
            return True
        except Exception as e:
            UIFormatter.print_error(f"Failed to create .env.sample file: {str(e)}")
            return False

    def create_app_urls(self) -> bool:
        """Create urls.py file in the app folder."""
        try:
            app_path = os.path.join(self.project_root, self.app_name)
            os.chdir(app_path)

            urls_content = f"""from django.urls import path
from . import views

app_name = '{self.app_name}'

urlpatterns = [
    # Add your URL patterns here
    # path('', views.index, name='index'),
]
"""

            with open("urls.py", "w") as file:
                file.write(urls_content)

            UIFormatter.print_success(f"Created {self.app_name}/urls.py")
            return True
        except Exception as e:
            UIFormatter.print_error(f"Failed to create app urls.py: {str(e)}")
            return False

    def update_project_urls(self) -> bool:
        """Update project urls.py with comprehensive URL configuration."""
        try:
            os.chdir(self.project_configs)

            urls_content = f"""from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # JWT tokens
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # App URLs
    path("", include("{self.app_name}.urls")),
]

# Don't show schema in production
if settings.DEBUG:
    urlpatterns += [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    ]
"""

            with open("urls.py", "w") as file:
                file.write(urls_content)

            self._format_file("urls.py")
            UIFormatter.print_success(
                "Updated project urls.py with comprehensive URL configuration"
            )
            return True
        except Exception as e:
            UIFormatter.print_error(f"Failed to update project urls.py: {str(e)}")
            return False

    def update_wsgi_file(self) -> bool:
        """Update wsgi.py with custom configuration."""
        try:
            os.chdir(self.project_configs)

            wsgi_content = """import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE"))

application = get_wsgi_application()
"""

            with open("wsgi.py", "w") as file:
                file.write(wsgi_content)

            self._format_file("wsgi.py")
            UIFormatter.print_success("Updated wsgi.py with custom configuration")
            return True
        except Exception as e:
            UIFormatter.print_error(f"Failed to update wsgi.py: {str(e)}")
            return False

    def update_asgi_file(self) -> bool:
        """Update asgi.py with custom configuration."""
        try:
            os.chdir(self.project_configs)

            asgi_content = """import os
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE"))

application = get_asgi_application()
"""

            with open("asgi.py", "w") as file:
                file.write(asgi_content)

            self._format_file("asgi.py")
            UIFormatter.print_success("Updated asgi.py with custom configuration")
            return True
        except Exception as e:
            UIFormatter.print_error(f"Failed to update asgi.py: {str(e)}")
            return False

    def update_manage_py(self) -> bool:
        """Update manage.py with custom configuration."""
        try:
            os.chdir(self.project_root)

            manage_content = """#!/usr/bin/env python
\"\"\"Django's command-line utility for administrative tasks.\"\"\"
import os
import sys
from dotenv import load_dotenv


def main():
    \"\"\"Run administrative tasks.\"\"\"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE"))

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    load_dotenv()
    main()
"""

            with open("manage.py", "w") as file:
                file.write(manage_content)

            self._format_file("manage.py")
            UIFormatter.print_success("Updated manage.py with custom configuration")
            return True
        except Exception as e:
            UIFormatter.print_error(f"Failed to update manage.py: {str(e)}")
            return False

    def _format_file(self, filename: str) -> None:
        """Format Python file using Black formatter."""
        try:
            subprocess.run(["black", filename], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # Black formatting failed, but file was still created
            pass
        except FileNotFoundError:
            # Black not installed, skip formatting
            pass
