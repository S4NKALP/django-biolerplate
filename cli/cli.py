"""
Main CLI orchestrator for Django project setup.
Coordinates between different managers to create a complete Django project.
"""

import os
from typing import List, Tuple, Callable

from .console import UIFormatter
from .project_manager import ProjectManager
from .settings_manager import SettingsManager
from .file_manager import FileManager


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

        # Create live progress display
        progress, task = UIFormatter.create_live_progress(total_steps)
        
        with progress:
            # Execute each step with progress tracking
            for step_number, (description, step_func) in enumerate(steps, 1):
                result = step_func()
                if not result:
                    success = False
                    UIFormatter.print_error(f"Step {step_number} failed: {description}")
                    break
                
                # Update the same progress bar
                progress.update(task, advance=1, description=f"Step {step_number}/{total_steps}")
        
        return success
    
    def _create_utility_files(self) -> bool:
        """Create all utility files for the project."""
        utility_steps = [
            self.file_manager.create_gitignore,
            self.file_manager.create_requirements,
            self.file_manager.create_readme,
            self.file_manager.create_env_file,
        ]
        
        for step_func in utility_steps:
            result = step_func()
            if not result:
                return False
        
        UIFormatter.print_success("Created all utility files successfully!")
        return True
