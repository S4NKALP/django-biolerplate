import os
import sys
import subprocess
import astor
import ast

try:
    # For when running as part of the package
    from .console import console
except ImportError:
    # For when running directly
    from console import console


class Cli:
    def __init__(self, project_name, app_name):
        self.django_project_name = project_name
        self.django_app_name = app_name
        self.project_root = os.path.join(os.getcwd(), self.django_project_name)
        self.project_configs = os.path.join(self.project_root, self.django_project_name)
        self.settings_folder = os.path.join(self.project_configs, "settings")
        self.settings_file = os.path.join(self.project_configs, "settings.py")

    def _create_project(self) -> bool:
        """
        Create a new Django project,
        return True if successful, False otherwise.
        """

        # check if a project already exists
        if not os.path.exists(self.project_root):
            try:
                import django
            except ImportError:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "django"],
                    check=True,
                )
                
            try:
                subprocess.run(
                    ["django-admin", "startproject", self.django_project_name],
                    check=True,
                )
                console.print(
                    f"\nDjango project '{self.django_project_name}' created successfully! ✅"
                )
                return True
            except Exception as e:
                return False
            
        else:
            console.print(f"\nDjango project already exists. ❌")
            return False

    def _create_app(self) -> bool:
        """Create a new Django app, return True if successful, False otherwise."""
        try:
            os.chdir(self.project_root)
            subprocess.run(
                [
                    sys.executable,
                    os.path.join(self.project_root, "manage.py"),
                    "startapp",
                    self.django_app_name,
                ],
                check=True,
            )
            console.print(
                f"\nDjango app '{self.django_app_name}' created successfully! ✅"
            )
            return True
        except Exception as e:
            # print("An error occurred while creating the Django app." + str(e)) # for debugging
            return False

    def _create_project_util_files(self) -> bool:
        """
        Creates:
            .gitignore,
            requirements.txt,
            README.md,
            .env.dev,
            .env.prod,

        returns: True if successful, False otherwise.
        """
        os.chdir(self.project_root)
        try:
            with open(".gitignore", "w") as file:
                file.write("*.pyc\n")
                file.write("__pycache__/\n")
                file.write("*.sqlite3\n")
                file.write("db.sqlite3\n")
                file.write("env\n")
                file.write(".env\n")
                file.write(".vscode\n")
                file.write(".idea\n")
                file.write("*.DS_Store\n")

            with open("requirements.txt", "w") as file:
                file.write("Django>=5.2.7\n")
                file.write("python-dotenv>=1.1.1\n")
                file.write("django-jazzmin>=3.0.1\n")
                file.write("djangorestframework>=3.16.1\n")
                file.write("djangorestframework_simplejwt>=5.5.1\n")
                file.write("drf-spectacular>=0.28.0\n")
                file.write("django-cors-headers>=4.9.0\n")
                file.write("whitenoise>=6.8.2\n")
            open("README.md", "a").close()
            with open(".env", "w") as file:
                file.write("# Django settings\n")
                file.write(f"DJANGO_SETTINGS_MODULE={self.django_project_name}.settings.development\n")
                file.write("SECRET_KEY=django-insecure-gs(+tg3%34((t$k(+6s5&n7b5@u)ruosu^&up00tr8ibuvml)a\n")
                file.write("ALLOWED_HOSTS=api.your-domain.com,www.your-domain.com\n")
                file.write("\n# Database\n")
                file.write("DB_NAME=\n")
                file.write("DB_USER=\n")
                file.write("DB_PASSWORD=\n")
                file.write("DB_HOST=\n")
                file.write("DB_PORT=\n")

            console.print(
                "\nCreated requirements.txt with Django dependencies, Readme, and .env files successfully! ✅"
            )
            return True
        except FileExistsError as e:
            # print(f"An error occurred while creating the project utility files. {e}") # for debugging
            return False

    def _create_settings(self) -> bool:
        """
        Creates a settings folder of the Django project.
        settings/base.py: Base settings
        settings/develoment.py: Development settings
        settings/production.py: Production settings

        returns: True if successful, False otherwise.
        """

        # cd into project folder
        os.chdir(self.project_configs)

        # create folder called settings
        os.makedirs("settings", exist_ok=True)

        # move into new folder
        os.chdir(self.settings_folder)

        # move settings.py into new settings folder and rename it to base.py
        os.rename(self.settings_file, os.path.join(self.settings_folder, "base.py"))

        try:
            open("__init__.py", "a").close()
            open("development.py", "a").close()
            open("production.py", "a").close()

            console.print(
                f"\nDjango project '{self.django_project_name}' Settings folder and files created successfully! ✅"
            )
            return True
        except FileExistsError as e:
            # print(F"An error occurred while creating the settings folder. {e}") # for debugging
            return False

    def _update_base_setting(self) -> bool:
        """
        Fill the base settings file with the necessary configurations.
        returns: True if successful, False otherwise.
        """
        try:
            # cd into project settings  folder
            os.chdir(self.settings_folder)

            # Complete base.py content
            base_content = f'''"""
Common settings shared between development and production environment

"""

from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/


# Application definition
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.token_blacklist",
    "corsheaders",
    "drf_spectacular",
]

USER_DEFINED_APPS = [
    "{self.django_app_name}"
]

BUILT_IN_APPS = [
    "jazzmin",
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

ROOT_URLCONF = "{self.django_project_name}.urls"

TEMPLATES = [
    {{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {{
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        }},
    }},
]

WSGI_APPLICATION = "{self.django_project_name}.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {{
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    }},
    {{
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    }},
    {{
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    }},
    {{
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    }},
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# staticfiles and mediafiles
STATIC_URL = "static/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework Settings
REST_FRAMEWORK = {{
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}}

# Custom SPECTACULAR_SETTINGS and SIMPLE_JWT settings change as you see fit
SPECTACULAR_SETTINGS = {{
    "TITLE": " ",
    "DESCRIPTION": "",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}}

SIMPLE_JWT = {{
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
}}
'''

            # Write the complete base.py file
            with open("base.py", "w") as file:
                file.write(base_content)

            # run black to format the code on base.py
            subprocess.run(["black", "base.py"], check=True)
            console.print(
                f"\nUpdated settings/base.py successfully! ✅"
            )
            return True
        except Exception as e:
            return False

    def _update_dev_setting(self) -> bool:
        """
        Fill the development settings file with the necessary configurations.
        returns: True if successful, False otherwise.
        """
        try:
            # cd into project settings folder
            os.chdir(self.settings_folder)

            # open development.py file
            with open("development.py", "w") as file:
                file.write("from .base import *\n\n")
                file.write("# SECURITY WARNING: keep the secret key used in production secret!\n")
                file.write('SECRET_KEY = "django-insecure-gs(+tg3%34((t$k(+6s5&n7b5@u)ruosu^&up00tr8ibuvml)a"\n\n')
                file.write("# SECURITY WARNING: don't run with debug turned on in production!\n")
                file.write("DEBUG = True\n\n")
                file.write('ALLOWED_HOSTS = ["*"]\n\n\n')
                file.write("# Database\n")
                file.write("# https://docs.djangoproject.com/en/5.2/ref/settings/#databases\n\n")
                file.write("DATABASES = {\n")
                file.write('    "default": {\n')
                file.write('        "ENGINE": "django.db.backends.sqlite3",\n')
                file.write('        "NAME": BASE_DIR / "db.sqlite3",\n')
                file.write("    }\n")
                file.write("}\n")

            console.print(
                f"\nUpdated settings/development.py successfully! ✅"
            )
            return True
        except Exception as e:
            # print(f"An error occurred while updating the development settings file. {e}") # for debugging
            return False

    def _update_prod_setting(self) -> bool:
        """
        Fill the production settings file with the necessary configurations.
        returns: True if successful, False otherwise.
        """

        try:
            # cd into project settings folder
            os.chdir(self.settings_folder)

            # open production.py file
            with open("production.py", "w") as file:
                file.write("from .base import *\n")
                file.write("import os\n\n")
                file.write("DEBUG = False\n")
                file.write("SECRET_KEY = os.getenv('SECRET_KEY')\n")
                file.write("ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')\n")
                file.write("\n# Database\n")
                file.write("DATABASES = {\n")
                file.write("    'default': {\n")
                file.write("        'ENGINE': 'django.db.backends.postgresql',\n")
                file.write("        'NAME': os.getenv('DB_NAME'),\n")
                file.write("        'USER': os.getenv('DB_USER'),\n")
                file.write("        'PASSWORD': os.getenv('DB_PASSWORD'),\n")
                file.write("        'HOST': os.getenv('DB_HOST'),\n")
                file.write("        'PORT': os.getenv('DB_PORT'),\n")
                file.write("    }\n")
                file.write("}\n")

            console.print(
                f"\nUpdated settings/production.py successfully! ✅"
            )
            return True
        except Exception as e:
            # print(f"An error occurred while updating the production settings file. {e}") # for debugging
            return False

    def _create_app_urls_file(self) -> bool:
        """
        create a urls.py file in the app folder.
        returns: True if successful, False otherwise.
        """

        try:
            # cd into the app folder
            os.chdir(os.path.join(self.project_root, self.django_app_name))

            # create urls.py file
            open("urls.py", "w").close()

            console.print(
                f"\nCreated '{self.django_app_name}/urls.py' successfully! ✅"
            )
            return True
        except Exception as e:
            return False

    def _add_app_urls_to_project_urls(self) -> bool:
        """
        Add the app urls to the project urls file.
        returns: True if successful, False otherwise.
        """
        os.chdir(self.project_configs)

        try:
            with open("urls.py", "r") as file:
                tree = ast.parse(file.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module == "django.urls":
                            # add the include function to the import statement, if it doesn't exist
                            if not any(alias.name == "include" for alias in node.names):
                                node.names.append(ast.alias(name="include", asname=None))

                for node in ast.walk(tree):
                        if isinstance(node, ast.Assign):
                            if node.targets[0].id == "urlpatterns":
                                node.value.elts.append(
                                    ast.Call(
                                    func=ast.Name(id="path", ctx=ast.Load()),
                                        args=[
                                        ast.Constant(s="", kind=None),
                                        ast.Name(id="include", ctx=ast.Load()),
                                        ast.Constant(s=f"{self.django_app_name}.urls", kind=None)
                                        ],
                                        keywords=[],
                                    )
                                )

            with open("urls.py", "w") as file:
                file.write(astor.to_source(tree))

            subprocess.run(["black", "urls.py"], check=True)
            console.print(f"\nAdded app urls to project urls.py successfully! ✅")
            return True
        except Exception as e:
            return False
    
    def _update_settings_path(self):
        """
        Updates manage.py setting path
        return True if successful False otherwise
        """
        try:
            os.chdir(self.project_root)

            with open("manage.py", "r") as file:
                tree = ast.parse(file.read())
                
                # Check if "from django.conf import settings" is already imported
                import_already_exists = any(
                    isinstance(node, ast.ImportFrom)
                    and node.module == "django.conf"
                    and any(alias.name == "settings" for alias in node.names)
                    for node in tree.body
                )

                # if not import_already_exists:
                #     env_import = ast.parse("from django.conf import settings").body[0]
                #     last_import_index = -1
                #     for index, node in enumerate(tree.body):
                #         if isinstance(node, (ast.Import, ast.ImportFrom)):
                #             last_import_index = index

                #     # Insert the new import after the last import statement
                #     tree.body.insert(last_import_index + 1, env_import)

                # Find and update the `os.environ.setdefault` call
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef) and node.name == "main":
                        for stmt in node.body:
                            if (
                                isinstance(stmt, ast.Expr)
                                and isinstance(stmt.value, ast.Call)
                                and isinstance(stmt.value.func, ast.Attribute)
                                and isinstance(stmt.value.func.value, ast.Attribute)
                                and isinstance(stmt.value.func.value.value, ast.Name)
                                and stmt.value.func.value.value.id == "os"
                                and stmt.value.func.value.attr == "environ"
                                and stmt.value.func.attr == "setdefault"
                            ):
                                # Update the second argument of the call
                                stmt.value.args[1] = ast.parse(
                                    f'os.getenv("DJANGO_SETTINGS_MODULE", "{self.django_project_name}.settings.development")'
                                ).body[0].value


            # write the changes to the file, with indentation and spaces
            with open("manage.py", "w") as file:
                file.write(astor.to_source(tree))

            subprocess.run(["black", "manage.py"], check=True)
            console.print(f"\nUpdated manage.py successfully! ✅")
            return True
        except Exception as e:
            return False

    def run_setup(self):
        """Main method that creates everything"""
        steps = [
            (self._create_project),
            (self._create_app),
            (self._create_settings),
            (self._update_base_setting),
            (self._update_dev_setting),
            (self._update_prod_setting),
            (self._create_project_util_files),
            (self._create_app_urls_file),
            (self._add_app_urls_to_project_urls),
            (self._update_settings_path),
        ]
        success = True

        for step in steps:
            result = step()
            if not result:
                success = False
                break
        
        if success:
            console.print(f"\nMake sure you set the env 'DJANGO_SETTINGS_MODULE' to '{self.django_project_name}.settings.development' (for your development environment)\nor '{self.django_project_name}.settings.production' (for your production environment) before running the server.")
