"""
Main script entry point for Django project setup.
Handles user input validation and orchestrates the setup process.
"""

import os
import re
import subprocess
import sys
from typing import Tuple

try:
    # For when running as part of the package
    from .cli import Cli
    from .console import UIColors, UIFormatter, console
except ImportError:
    # For when running directly
    from console import UIColors, UIFormatter, console

    from cli import Cli


def validate_project_name(name: str) -> Tuple[bool, str]:
    """Validate Django project name according to Django conventions."""
    if not name or not name.strip():
        return False, "Project name cannot be empty"

    name = name.strip()

    # Check for reserved names
    reserved_names = {
        "test",
        "tests",
        "django",
        "admin",
        "api",
        "static",
        "media",
        "manage",
        "settings",
        "urls",
        "wsgi",
        "asgi",
        "models",
        "views",
    }
    if name.lower() in reserved_names:
        return False, f"'{name}' is a reserved name. Please choose a different name."

    # Check naming pattern
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name):
        return (
            False,
            "Project name must start with a letter and contain only letters, numbers, and underscores",
        )

    # Check length constraints
    if len(name) < 2:
        return False, "Project name must be at least 2 characters long"

    if len(name) > 50:
        return False, "Project name must be less than 50 characters"

    # Check for Python keywords
    import keyword

    if keyword.iskeyword(name):
        return False, f"'{name}' is a Python keyword. Please choose a different name."

    return True, ""


def validate_app_name(name: str) -> Tuple[bool, str]:
    """Validate Django app name according to Django conventions."""
    if not name or not name.strip():
        return False, "App name cannot be empty"

    name = name.strip()

    # Check for reserved names
    reserved_names = {
        "test",
        "tests",
        "django",
        "admin",
        "api",
        "static",
        "media",
        "manage",
        "settings",
        "urls",
        "wsgi",
        "asgi",
        "models",
        "views",
    }
    if name.lower() in reserved_names:
        return False, f"'{name}' is a reserved name. Please choose a different name."

    # Check naming pattern
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name):
        return (
            False,
            "App name must start with a letter and contain only letters, numbers, and underscores",
        )

    # Check length constraints
    if len(name) < 2:
        return False, "App name must be at least 2 characters long"

    if len(name) > 50:
        return False, "App name must be less than 50 characters"

    # Check for Python keywords
    import keyword

    if keyword.iskeyword(name):
        return False, f"'{name}' is a Python keyword. Please choose a different name."

    return True, ""


def get_user_input() -> Tuple[str, str]:
    """Get validated input from user with improved error handling."""
    console.print()

    # Get project name with validation
    project_name = _get_validated_input(
        "Enter the Django project name", validate_project_name, "project name"
    )

    # Get app name with validation
    app_name = _get_validated_input(
        "Enter the Django app name", validate_app_name, "app name"
    )

    return project_name, app_name


def _get_validated_input(prompt: str, validator, input_type: str) -> str:
    """Get validated input from user with retry logic."""
    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        try:
            user_input = console.input(
                f"[{UIColors.HIGHLIGHT}]{prompt}:[/{UIColors.HIGHLIGHT}] "
            )
            is_valid, error_msg = validator(user_input)

            if is_valid:
                return user_input.strip()
            else:
                UIFormatter.print_error(error_msg)
                attempt += 1
                if attempt < max_attempts:
                    console.print(
                        f"[{UIColors.MUTED}]Please try again ({attempt}/{max_attempts}).[/{UIColors.MUTED}]"
                    )
                else:
                    UIFormatter.print_error(
                        f"Maximum attempts reached for {input_type}. Exiting."
                    )
                    sys.exit(1)
        except KeyboardInterrupt:
            UIFormatter.print_info("\nSetup cancelled by user.")
            sys.exit(0)
        except Exception as e:
            UIFormatter.print_error(f"Unexpected error: {str(e)}")
            attempt += 1

    # This should never be reached due to sys.exit(1) above
    raise RuntimeError("Validation failed unexpectedly")


def clear_screen() -> None:
    """Clear the terminal screen."""
    try:
        if os.name == "nt":
            subprocess.run("cls", shell=True, check=True)  # Windows
        else:
            subprocess.run("clear", shell=True, check=True)  # Linux/MacOS
    except subprocess.CalledProcessError:
        # If clearing fails, just print some newlines
        console.print("\n" * 50)


def confirm_setup(project_name: str, app_name: str) -> bool:
    """Confirm setup with user before proceeding."""
    console.print()
    console.print(f"[{UIColors.INFO}]Project:[/{UIColors.INFO}] {project_name}")
    console.print(f"[{UIColors.INFO}]App:[/{UIColors.INFO}] {app_name}")
    console.print()

    try:
        response = console.input(
            f"[{UIColors.WARNING}]Proceed with setup? (y/N):[/{UIColors.WARNING}] "
        )
        return response.lower().startswith("y")
    except KeyboardInterrupt:
        UIFormatter.print_info("\nSetup cancelled by user.")
        return False


def main() -> None:
    """Main entry point for the Django setup script."""
    try:
        # Clear screen
        clear_screen()

        # Display welcome screen
        console.print()
        console.print(UIFormatter.create_welcome_panel())
        console.print()

        # Get user input
        project_name, app_name = get_user_input()

        # Confirm setup
        if not confirm_setup(project_name, app_name):
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

        # Exit with appropriate code
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        UIFormatter.print_info("\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        UIFormatter.print_error(f"Unexpected error: {str(e)}")
        console.print(
            f"[{UIColors.MUTED}]Please check your environment and try again.[/{UIColors.MUTED}]"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

