from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
from rich.syntax import Syntax
from rich.markdown import Markdown
import time

console = Console()

class UIColors:
    """Enhanced color scheme for modern UI styling"""
    SUCCESS = "bold green"
    ERROR = "bold red"
    WARNING = "bold yellow"
    INFO = "bold blue"
    HIGHLIGHT = "bold cyan"
    MUTED = "dim white"
    ACCENT = "bold magenta"
    PRIMARY = "bold white"
    SECONDARY = "bright_white"

class UIFormatter:
    """Utility class for consistent UI formatting"""
    
    @staticmethod
    def print_success(message: str):
        """Print success message with enhanced styling"""
        console.print(f"[{UIColors.SUCCESS}]✓[/{UIColors.SUCCESS}] [bold]{message}[/bold]")
    
    @staticmethod
    def print_error(message: str):
        """Print error message with enhanced styling"""
        console.print(f"[{UIColors.ERROR}]✗[/{UIColors.ERROR}] [bold]{message}[/bold]")
    
    @staticmethod
    def print_warning(message: str):
        """Print warning message with enhanced styling"""
        console.print(f"[{UIColors.WARNING}]⚠[/{UIColors.WARNING}] [bold]{message}[/bold]")
    
    @staticmethod
    def print_info(message: str):
        """Print info message with enhanced styling"""
        console.print(f"[{UIColors.INFO}]ℹ[/{UIColors.INFO}] [bold]{message}[/bold]")
    
    @staticmethod
    def print_step(step_number: int, total_steps: int, description: str):
        """Print step information with enhanced progress indicator"""
        console.print(f"[{UIColors.HIGHLIGHT}]Step {step_number}/{total_steps}:[/{UIColors.HIGHLIGHT}] {description}")
    
    @staticmethod
    def print_progress_bar(step_number: int, total_steps: int):
        """Print a single progress bar that shows overall progress"""
        progress_percentage = int((step_number / total_steps) * 100)
        progress_bar = "█" * int((step_number / total_steps) * 30)
        remaining = "░" * (30 - len(progress_bar))
        console.print(f"\r[{UIColors.ACCENT}][{progress_bar}{remaining}][/{UIColors.ACCENT}] {progress_percentage}%", end="")
    
    @staticmethod
    def create_live_progress(total_steps: int):
        """Create a live progress display that updates in place"""
        from rich.live import Live
        from rich.progress import Progress, BarColumn, TextColumn, TaskProgressColumn
        
        progress = Progress(
            TextColumn("[bold blue]Setup Progress:"),
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            console=console
        )
        
        task = progress.add_task("", total=total_steps)
        return progress, task
    
    @staticmethod
    def print_header(text: str):
        """Print a styled header"""
        console.print(f"\n[{UIColors.PRIMARY}]{'=' * 60}[/{UIColors.PRIMARY}]")
        console.print(f"[{UIColors.PRIMARY}]{text.center(60)}[/{UIColors.PRIMARY}]")
        console.print(f"[{UIColors.PRIMARY}]{'=' * 60}[/{UIColors.PRIMARY}]\n")
    
    @staticmethod
    def print_separator():
        """Print a visual separator"""
        console.print(f"[{UIColors.MUTED}]{'─' * 60}[/{UIColors.MUTED}]")
    
    @staticmethod
    def print_feature_list(features: list):
        """Print a styled feature list"""
        for i, feature in enumerate(features, 1):
            console.print(f"[{UIColors.ACCENT}]  {i}.[/{UIColors.ACCENT}] [bold]{feature}[/bold]")
    
    @staticmethod
    def print_code_block(code: str, language: str = "python"):
        """Print code with syntax highlighting"""
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        console.print(syntax)
    
    @staticmethod
    def create_welcome_panel():
        """Create an enhanced welcome panel with ASCII art header"""
        welcome_text = Text()
        
        # ASCII Art Header
        ascii_art = """
      _ _                           _       _ _   
     | (_)                         (_)     (_) |  
   __| |_  __ _ _ __   __ _  ___    _ _ __  _| |_ 
  / _` | |/ _` | '_ \ / _` |/ _ \  | | '_ \| | __|
 | (_| | | (_| | | | | (_| | (_) | | | | | | | |_ 
  \__,_| |\__,_|_| |_|\__, |\___/  |_|_| |_|_|\__|
      _/ |             __/ |                      
     |__/             |___/                       

  Django Project Setup Tool
  Create production-ready Django projects with modern architecture

  Repository: https://github.com/S4NKALP/django-init
  License: MIT
"""
        
        welcome_text.append(ascii_art, style=UIColors.ACCENT)
        welcome_text.append("\n")
        return welcome_text
    
    @staticmethod
    def create_summary_panel(project_name: str, app_name: str, success: bool):
        """Create an enhanced completion summary panel"""
        if success:
            title = "[bold green]🎉 Setup Complete![/bold green]"
            border_style = "green"
            
            summary_text = Text()
            summary_text.append("🎯 Project Details:\n", style="bold cyan")
            summary_text.append(f"📁 Project: ", style=UIColors.PRIMARY)
            summary_text.append(f"{project_name}\n", style="bold white")
            summary_text.append(f"📱 App: ", style=UIColors.PRIMARY)
            summary_text.append(f"{app_name}\n\n", style="bold white")
            
            summary_text.append("🚀 Next Steps:\n", style="bold cyan")
            steps = [
                "Navigate to your project directory",
                "Set environment variables in .env file", 
                "Run migrations: python manage.py migrate",
                "Create superuser: python manage.py createsuperuser",
                "Start development server: python manage.py runserver"
            ]
            
            for i, step in enumerate(steps, 1):
                summary_text.append(f"  {i}. {step}\n", style=UIColors.MUTED)
            
            summary_text.append("\n🔗 Useful URLs:\n", style="bold cyan")
            summary_text.append("  • Admin: http://localhost:8000/admin/\n", style=UIColors.MUTED)
            summary_text.append("  • API Docs: http://localhost:8000/docs/\n", style=UIColors.MUTED)
            summary_text.append("  • API Schema: http://localhost:8000/schema/\n", style=UIColors.MUTED)
            
        else:
            title = "[bold red]❌ Setup Failed[/bold red]"
            border_style = "red"
            
            summary_text = Text()
            summary_text.append("The setup process encountered an error.\n\n", style="red")
            summary_text.append("🔍 Troubleshooting Tips:\n", style="bold yellow")
            summary_text.append("  • Check the error messages above\n", style=UIColors.MUTED)
            summary_text.append("  • Ensure you have write permissions\n", style=UIColors.MUTED)
            summary_text.append("  • Verify Django is installed correctly\n", style=UIColors.MUTED)
            summary_text.append("  • Try running with elevated permissions\n", style=UIColors.MUTED)
        
        return Panel(
            summary_text,
            title=title,
            border_style=border_style,
            padding=(2, 3),
            box=box.DOUBLE
        )
    
    @staticmethod
    def create_progress_display(total_steps: int):
        """Create a live progress display"""
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        )
        return progress
    
    @staticmethod
    def create_feature_table():
        """Create a feature comparison table"""
        table = Table(title="🚀 Django Setup Features", show_header=True, header_style="bold cyan")
        table.add_column("Feature", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Status", justify="center", style="green")
        
        features = [
            ("Project Structure", "Environment-specific settings", "✅"),
            ("REST API", "JWT authentication & permissions", "✅"),
            ("Admin Interface", "Beautiful Jazzmin admin panel", "✅"),
            ("API Documentation", "Swagger UI & OpenAPI schema", "✅"),
            ("CORS Support", "Frontend integration ready", "✅"),
            ("Production Ready", "Security & performance optimized", "✅"),
            ("Logging", "Comprehensive error tracking", "✅"),
            ("Database", "SQLite (dev) / PostgreSQL (prod)", "✅")
        ]
        
        for feature, description, status in features:
            table.add_row(feature, description, status)
        
        return table