"""
Project management for Django project setup.
Handles creation of Django projects and apps.
"""

import os
import sys
import subprocess
from typing import Optional

try:
    from .console import UIFormatter
except ImportError:
    from console import UIFormatter


class ProjectManager:
    """Manages Django project and app creation."""
    
    def __init__(self, project_name: str, app_name: str):
        self.project_name = project_name
        self.app_name = app_name
        self.project_root = os.path.join(os.getcwd(), project_name)
    
    def create_project(self) -> bool:
        """Create a new Django project."""
        # Check if project already exists
        if os.path.exists(self.project_root):
            UIFormatter.print_error(f"Django project '{self.project_name}' already exists.")
            UIFormatter.print_info("Please choose a different project name or remove the existing directory.")
            return False
        
        try:
            # Ensure Django is installed
            self._ensure_django_installed()
            
            # Create Django project
            subprocess.run(
                ["django-admin", "startproject", self.project_name],
                check=True,
            )
            
            UIFormatter.print_success(f"Django project '{self.project_name}' created successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            UIFormatter.print_error(f"Failed to create Django project: {str(e)}")
            UIFormatter.print_info("Make sure Django is installed and you have write permissions in the current directory.")
            return False
        except Exception as e:
            UIFormatter.print_error(f"Unexpected error creating project: {str(e)}")
            return False
    
    def create_app(self) -> bool:
        """Create a new Django app."""
        try:
            # Change to project directory
            original_cwd = os.getcwd()
            os.chdir(self.project_root)
            
            # Create Django app
            subprocess.run(
                [
                    sys.executable,
                    os.path.join(self.project_root, "manage.py"),
                    "startapp",
                    self.app_name,
                ],
                check=True,
            )
            
            UIFormatter.print_success(f"Django app '{self.app_name}' created successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            UIFormatter.print_error(f"Failed to create Django app: {str(e)}")
            UIFormatter.print_info("Make sure you're in the correct project directory and have write permissions.")
            return False
        except Exception as e:
            UIFormatter.print_error(f"Unexpected error creating app: {str(e)}")
            return False
        finally:
            # Always return to original directory
            try:
                os.chdir(original_cwd)
            except OSError:
                pass  # Directory might not exist anymore
    
    def _ensure_django_installed(self) -> None:
        """Ensure Django is installed, install if not."""
        try:
            import django
        except ImportError:
            UIFormatter.print_info("Django not found, installing...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "django"],
                check=True,
            )
            UIFormatter.print_success("Django installed successfully!")
    
    def validate_project_structure(self) -> bool:
        """Validate that the project structure is correct."""
        required_files = [
            os.path.join(self.project_root, "manage.py"),
            os.path.join(self.project_root, self.project_name, "__init__.py"),
            os.path.join(self.project_root, self.project_name, "settings.py"),
            os.path.join(self.project_root, self.project_name, "urls.py"),
            os.path.join(self.project_root, self.project_name, "wsgi.py"),
            os.path.join(self.project_root, self.project_name, "asgi.py"),
            os.path.join(self.project_root, self.app_name, "__init__.py"),
            os.path.join(self.project_root, self.app_name, "apps.py"),
            os.path.join(self.project_root, self.app_name, "models.py"),
            os.path.join(self.project_root, self.app_name, "views.py"),
            os.path.join(self.project_root, self.app_name, "admin.py"),
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            UIFormatter.print_error("Project structure validation failed:")
            for file_path in missing_files:
                UIFormatter.print_error(f"  Missing: {file_path}")
            return False
        
        UIFormatter.print_success("Project structure validation passed")
        return True
