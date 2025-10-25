import os
import subprocess
import re
try:
    # For when running as part of the package
    from .console import console, UIFormatter, UIColors
    from .cli import Cli
except ImportError:
    # For when running directly
    from console import console, UIFormatter, UIColors
    from cli import Cli

def validate_project_name(name: str) -> tuple[bool, str]:
    """Validate Django project name according to Django conventions"""
    if not name:
        return False, "Project name cannot be empty"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
        return False, "Project name must start with a letter and contain only letters, numbers, and underscores"
    
    if len(name) < 2:
        return False, "Project name must be at least 2 characters long"
    
    if len(name) > 50:
        return False, "Project name must be less than 50 characters"
    
    return True, ""

def validate_app_name(name: str) -> tuple[bool, str]:
    """Validate Django app name according to Django conventions"""
    if not name:
        return False, "App name cannot be empty"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
        return False, "App name must start with a letter and contain only letters, numbers, and underscores"
    
    if len(name) < 2:
        return False, "App name must be at least 2 characters long"
    
    if len(name) > 50:
        return False, "App name must be less than 50 characters"
    
    return True, ""

def get_user_input():
    """Get validated input from user"""
    console.print()
    
    # Get project name with validation
    while True:
        project_name = console.input(f"[{UIColors.HIGHLIGHT}]Enter the Django project name:[/{UIColors.HIGHLIGHT}] ")
        is_valid, error_msg = validate_project_name(project_name)
        
        if is_valid:
            break
        else:
            UIFormatter.print_error(error_msg)
            console.print(f"[{UIColors.MUTED}]Please try again.[/{UIColors.MUTED}]")
    
    # Get app name with validation
    while True:
        app_name = console.input(f"[{UIColors.HIGHLIGHT}]Enter the Django app name:[/{UIColors.HIGHLIGHT}] ")
        is_valid, error_msg = validate_app_name(app_name)
        
        if is_valid:
            break
        else:
            UIFormatter.print_error(error_msg)
            console.print(f"[{UIColors.MUTED}]Please try again.[/{UIColors.MUTED}]")
    
    return project_name, app_name

def main():
    # Clear screen
    if os.name == 'nt':
        subprocess.run('cls', shell=True) # Windows
    else:
        subprocess.run('clear', shell=True) # Linux/MacOS

    # Display welcome screen
    console.print()
    console.print(UIFormatter.create_welcome_panel())
    console.print()

    # Get user input
    project_name, app_name = get_user_input()
    
    # Confirm setup
    console.print()
    console.print(f"[{UIColors.INFO}]Project:[/{UIColors.INFO}] {project_name}")
    console.print(f"[{UIColors.INFO}]App:[/{UIColors.INFO}] {app_name}")
    console.print()
    
    if not console.input(f"[{UIColors.WARNING}]Proceed with setup? (y/N):[/{UIColors.WARNING}] ").lower().startswith('y'):
        UIFormatter.print_info("Setup cancelled by user.")
        return

    # Run setup
    console.print()
    UIFormatter.print_info("Starting Django project setup...")
    console.print()
    
    django_cli = Cli(project_name, app_name)
    success = django_cli.run_setup()
    
    # Display completion summary
    console.print()
    console.print(UIFormatter.create_summary_panel(project_name, app_name, success))
    console.print()

if __name__ == "__main__":
    main()