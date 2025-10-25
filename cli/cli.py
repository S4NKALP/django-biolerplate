"""
Main CLI orchestrator for Django project setup.
Coordinates between different managers to create a complete Django project.
"""

import os
from typing import List, Tuple, Callable

try:
    # For when running as part of the package
    from .console import UIFormatter
    from .project_manager import ProjectManager
    from .settings_manager import SettingsManager
    from .file_manager import FileManager
except ImportError:
    # For when running directly
    from console import UIFormatter
    from project_manager import ProjectManager
    from settings_manager import SettingsManager
    from file_manager import FileManager


class Cli:
    """Main CLI orchestrator for Django project setup."""
    
    def __init__(self, project_name: str, app_name: str):
        self.project_name = project_name
        self.app_name = app_name
        self.project_root = os.path.join(os.getcwd(), project_name)
        
        # Initialize managers
        self.project_manager = ProjectManager(project_name, app_name)
        self.settings_manager = SettingsManager(self.project_root, project_name, app_name)
        self.file_manager = FileManager(self.project_root, project_name, app_name)

    def run_setup(self) -> bool:
        """Main method that orchestrates the complete Django project setup."""
        # Define setup steps with their descriptions and corresponding methods
        steps: List[Tuple[str, Callable[[], bool]]] = [
            ("Creating Django project", self.project_manager.create_project),
            ("Creating Django app", self.project_manager.create_app),
            ("Validating project structure", self.project_manager.validate_project_structure),
            ("Setting up project structure", self.settings_manager.create_settings_structure),
            ("Configuring base settings", self.settings_manager.update_base_settings),
            ("Configuring development settings", self.settings_manager.update_development_settings),
            ("Configuring production settings", self.settings_manager.update_production_settings),
            ("Creating utility files", self._create_utility_files),
            ("Setting up app URLs", self.file_manager.create_app_urls),
            ("Configuring comprehensive URLs", self.file_manager.update_project_urls),
            ("Updating WSGI configuration", self.file_manager.update_wsgi_file),
            ("Updating ASGI configuration", self.file_manager.update_asgi_file),
            ("Updating manage.py", self.file_manager.update_manage_py),
        ]
        
        total_steps = len(steps)
        success = True

        # Execute each step with progress tracking
        for step_number, (description, step_func) in enumerate(steps, 1):
            UIFormatter.print_step(step_number, total_steps, description)
            
            try:
                result = step_func()
                if not result:
                    success = False
                    UIFormatter.print_error(f"Step {step_number} failed: {description}")
                    break
            except Exception as e:
                success = False
                UIFormatter.print_error(f"Unexpected error in step {step_number}: {str(e)}")
                break
        
        return success
    
    def _create_utility_files(self) -> bool:
        """Create all utility files for the project."""
        utility_steps = [
            ("Creating .gitignore", self.file_manager.create_gitignore),
            ("Creating requirements.txt", self.file_manager.create_requirements),
            ("Creating README.md", self.file_manager.create_readme),
            ("Creating .env file", self.file_manager.create_env_file),
        ]
        
        for description, step_func in utility_steps:
            try:
                result = step_func()
                if not result:
                    UIFormatter.print_error(f"Failed to {description.lower()}")
                    return False
            except Exception as e:
                UIFormatter.print_error(f"Unexpected error while {description.lower()}: {str(e)}")
                return False
        
        UIFormatter.print_success("Created all utility files successfully!")
        return True
