from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


class UIColors:
    """Color scheme for consistent UI styling"""

    SUCCESS = "green"
    ERROR = "red"
    WARNING = "yellow"
    INFO = "blue"
    HIGHLIGHT = "cyan"
    MUTED = "dim white"


class UIFormatter:
    """Utility class for consistent UI formatting"""

    @staticmethod
    def print_success(message: str):
        """Print success message with consistent styling"""
        console.print(f"[{UIColors.SUCCESS}]✓[/{UIColors.SUCCESS}] {message}")

    @staticmethod
    def print_error(message: str):
        """Print error message with consistent styling"""
        console.print(f"[{UIColors.ERROR}]✗[/{UIColors.ERROR}] {message}")

    @staticmethod
    def print_warning(message: str):
        """Print warning message with consistent styling"""
        console.print(f"[{UIColors.WARNING}]⚠[/{UIColors.WARNING}] {message}")

    @staticmethod
    def print_info(message: str):
        """Print info message with consistent styling"""
        console.print(f"[{UIColors.INFO}]ℹ[/{UIColors.INFO}] {message}")

    @staticmethod
    def print_step(step_number: int, total_steps: int, description: str):
        """Print step information with progress indicator"""
        console.print(
            f"[{UIColors.HIGHLIGHT}]Step {step_number}/{total_steps}:[/{UIColors.HIGHLIGHT}] {description}"
        )

    @staticmethod
    def create_welcome_panel():
        """Create an attractive welcome panel"""
        welcome_text = Text()
        welcome_text.append("Django Project Setup Tool", style="bold cyan")
        welcome_text.append("\n\n")
        welcome_text.append(
            "This tool will help you create a Django project with:\n",
            style=UIColors.MUTED,
        )
        welcome_text.append(
            "• Modern project structure with environment-specific settings\n",
            style=UIColors.MUTED,
        )
        welcome_text.append(
            "• Pre-configured REST API with JWT authentication\n", style=UIColors.MUTED
        )
        welcome_text.append(
            "• Essential dependencies and utilities\n", style=UIColors.MUTED
        )
        welcome_text.append("• Production-ready configuration\n", style=UIColors.MUTED)

        return Panel(
            welcome_text,
            title="[bold green]Welcome![/bold green]",
            border_style="green",
            padding=(1, 2),
            box=box.ROUNDED,
        )

    @staticmethod
    def create_summary_panel(project_name: str, app_name: str, success: bool):
        """Create a completion summary panel"""
        if success:
            title = "[bold green]Setup Complete![/bold green]"
            border_style = "green"

            summary_text = Text()
            summary_text.append(f"Project: {project_name}\n", style="bold")
            summary_text.append(f"App: {app_name}\n\n", style="bold")
            summary_text.append("Next Steps:\n", style="bold cyan")
            summary_text.append(
                "1. Navigate to your project directory\n", style=UIColors.MUTED
            )
            summary_text.append(
                "2. Set environment variables in .env file\n", style=UIColors.MUTED
            )
            summary_text.append(
                "3. Run migrations: python manage.py migrate\n", style=UIColors.MUTED
            )
            summary_text.append(
                "4. Create superuser: python manage.py createsuperuser\n",
                style=UIColors.MUTED,
            )
            summary_text.append(
                "5. Start development server: python manage.py runserver\n",
                style=UIColors.MUTED,
            )
        else:
            title = "[bold red]Setup Failed[/bold red]"
            border_style = "red"

            summary_text = Text()
            summary_text.append(
                "The setup process encountered an error.\n\n", style="red"
            )
            summary_text.append(
                "Please check the error messages above and try again.\n",
                style=UIColors.MUTED,
            )
            summary_text.append(
                "Make sure you have the necessary permissions and dependencies.\n",
                style=UIColors.MUTED,
            )

        return Panel(
            summary_text,
            title=title,
            border_style=border_style,
            padding=(1, 2),
            box=box.ROUNDED,
        )

