"""
Feature definitions for the Django boilerplate generator.
Each feature defines its dependencies, settings, and template modifications.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Feature:
    """Represents a feature that can be included in the Django project."""

    name: str
    description: str
    dependencies: List[str]
    apps: List[str]
    middleware: List[str]
    settings: Dict[str, any]
    production_settings: Dict[str, any]  # Production-specific settings
    requirements: List[str]
    template_files: List[
        str
    ]  # Files that should be included when this feature is selected


# Define all available features
FEATURES = {
    "drf": Feature(
        name="Django REST Framework",
        description="Add Django REST Framework for building APIs",
        dependencies=[],
        apps=["rest_framework"],
        middleware=[],
        settings={
            "REST_FRAMEWORK": {
                "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
                "PAGE_SIZE": 10,
                "DEFAULT_AUTHENTICATION_CLASSES": [
                    "rest_framework.authentication.SessionAuthentication",
                ],
                "DEFAULT_PERMISSION_CLASSES": [
                    "rest_framework.permissions.IsAuthenticated",
                ],
            }
        },
        production_settings={},
        requirements=["djangorestframework==3.16.0"],
        template_files=["__APP__/serializers.py", "__APP__/views.py"],
    ),
    "api_docs": Feature(
        name="API Documentation (drf-yasg)",
        description="Add Swagger/OpenAPI documentation for APIs",
        dependencies=["drf"],
        apps=["drf_yasg"],
        middleware=[],
        settings={
            "REST_FRAMEWORK": {
                "DEFAULT_SCHEMA_CLASS": "drf_yasg.openapi.AutoSchema",
            }
        },
        production_settings={},
        requirements=["drf-yasg==1.21.10"],
        template_files=[],
    ),
    "cors": Feature(
        name="CORS Headers",
        description="Add Cross-Origin Resource Sharing support",
        dependencies=[],
        apps=["corsheaders"],
        middleware=["corsheaders.middleware.CorsMiddleware"],
        settings={
            "CORS_ALLOWED_ORIGINS": "_split_env_list(os.environ.get('CORS_ALLOWED_ORIGINS'))",
            "CORS_ALLOW_ALL_ORIGINS": "(os.environ.get('CORS_ALLOW_ALL_ORIGINS') or '').lower() in ('1', 'true', 'yes', 'on') or (not CORS_ALLOWED_ORIGINS and DEBUG)",
            "CORS_ALLOW_CREDENTIALS": "(os.environ.get('CORS_ALLOW_CREDENTIALS', 'True').lower() in ('1', 'true', 'yes', 'on'))",
            "CORS_ALLOWED_METHODS": [
                "DELETE",
                "GET",
                "OPTIONS",
                "PATCH",
                "POST",
                "PUT",
            ],
        },
        production_settings={},
        requirements=["django-cors-headers==4.7.0"],
        template_files=[],
    ),
    "whitenoise": Feature(
        name="WhiteNoise (Static Files)",
        description="Add WhiteNoise for serving static files in production",
        dependencies=[],
        apps=[],
        middleware=["whitenoise.middleware.WhiteNoiseMiddleware"],
        settings={},
        production_settings={
            "STORAGES": {
                "staticfiles": {
                    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
                },
            }
        },
        requirements=["whitenoise==6.9.0"],
        template_files=[],
    ),
    "jazzmin": Feature(
        name="Django Jazzmin (Admin UI)",
        description="Add Jazzmin for a modern admin interface",
        dependencies=[],
        apps=["jazzmin"],
        middleware=[],
        settings={},
        production_settings={},
        requirements=["django-jazzmin==3.0.1"],
        template_files=[],
    ),
    "database_url": Feature(
        name="Database URL Support",
        description="Add support for DATABASE_URL environment variable",
        dependencies=[],
        apps=[],
        middleware=[],
        settings={},
        production_settings={},
        requirements=["dj-database-url>=2,<3"],
        template_files=[],
    ),
    "email": Feature(
        name="Email Configuration",
        description="Add email configuration for production",
        dependencies=[],
        apps=[],
        middleware=[],
        settings={},
        production_settings={
            "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
            "EMAIL_HOST": "smtp.gmail.com",
            "EMAIL_PORT": 587,
            "EMAIL_USE_TLS": True,
            "EMAIL_HOST_USER": "os.environ.get('EMAIL_HOST_USER')",
            "EMAIL_HOST_PASSWORD": "os.environ.get('EMAIL_HOST_PASSWORD')",
            "DEFAULT_FROM_EMAIL": "EMAIL_HOST_USER",
        },
        requirements=[],
        template_files=[],
    ),
    "security": Feature(
        name="Production Security",
        description="Add production security settings (SSL, HSTS, etc.)",
        dependencies=[],
        apps=[],
        middleware=[],
        settings={},
        production_settings={
            "SECURE_PROXY_SSL_HEADER": "('HTTP_X_FORWARDED_PROTO', 'https')",
            "SECURE_SSL_REDIRECT": True,
            "SESSION_COOKIE_SECURE": True,
            "CSRF_COOKIE_SECURE": True,
            "SECURE_HSTS_SECONDS": "60 * 60 * 24 * 30",
            "SECURE_HSTS_INCLUDE_SUBDOMAINS": True,
            "SECURE_HSTS_PRELOAD": True,
        },
        requirements=[],
        template_files=[],
    ),
    "environ": Feature(
        name="Django Environ",
        description="Add django-environ for environment variable management",
        dependencies=[],
        apps=[],
        middleware=[],
        settings={},
        production_settings={},
        requirements=["django-environ>=0.11,<1"],
        template_files=[],
    ),
}


def get_feature_dependencies(feature_name: str) -> List[str]:
    """Get all dependencies for a feature, including transitive dependencies."""
    if feature_name not in FEATURES:
        return []

    dependencies = set()
    to_process = [feature_name]

    while to_process:
        current = to_process.pop(0)
        if current in dependencies:
            continue
        dependencies.add(current)

        feature = FEATURES[current]
        to_process.extend(feature.dependencies)

    return list(dependencies)


def get_selected_features_config(selected_features: List[str]) -> Dict:
    """Generate configuration for selected features."""
    all_apps = set()
    all_middleware = []
    all_requirements = set()
    all_settings = {}
    all_production_settings = {}

    # Add core Django requirements
    all_requirements.update(
        ["asgiref==3.9.1", "Django==5.2.6", "sqlparse==0.5.3", "requests==2.32.4"]
    )

    # Get all features including dependencies
    all_features = set()
    for feature_name in selected_features:
        all_features.update(get_feature_dependencies(feature_name))

    for feature_name in all_features:
        if feature_name not in FEATURES:
            continue

        feature = FEATURES[feature_name]
        all_apps.update(feature.apps)
        all_middleware.extend(feature.middleware)
        all_requirements.update(feature.requirements)
        all_settings.update(feature.settings)
        all_production_settings.update(feature.production_settings)

    return {
        "apps": list(all_apps),
        "middleware": all_middleware,
        "requirements": list(all_requirements),
        "settings": all_settings,
        "production_settings": all_production_settings,
    }
