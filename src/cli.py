import argparse
import importlib.resources as pkg_resources
import re
import shutil
import subprocess
import sys
from pathlib import Path

TEXT_EXTS = {
    ".py",
    ".txt",
    ".md",
    ".env",
    ".yml",
    ".yaml",
    ".json",
    ".html",
    ".css",
    ".js",
    ".ini",
    ".cfg",
}


def valid_name(name):
    return re.match(r"^[a-zA-Z][_a-zA-Z0-9]+$", name) is not None


def render_and_copy(src: Path, dst: Path, replacements: dict):
    """Recursively copy files and replace placeholders."""
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        for child in src.iterdir():
            new_name = child.name.replace(
                "__PROJECT__", replacements["project_name"]
            ).replace("__APP__", replacements["app_name"])
            render_and_copy(child, dst / new_name, replacements)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix.lower() in TEXT_EXTS or src.name in {"Dockerfile", ".gitignore"}:
            text = src.read_text(encoding="utf-8")
            text = text.replace("{{ project_name }}", replacements["project_name"])
            text = text.replace("{{ app_name }}", replacements["app_name"])
            dst.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(src, dst)


def run():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a Django project from a boilerplate."
    )
    parser.add_argument("--project", "-p", help="Django project name")
    parser.add_argument("--app", "-a", help="Default app name")
    parser.add_argument("--git", action="store_true", help="Initialize Git repo")
    args = parser.parse_args()

    project_name = args.project or input("Enter your Django project name: ").strip()
    app_name = args.app or input("Enter your first Django app name: ").strip()

    if not valid_name(project_name) or not valid_name(app_name):
        print(
            "Project and app names must start with a letter and contain only letters, numbers, and underscores."
        )
        sys.exit(1)

    base_dir = Path.cwd()

    # Step 1: Create Django project
    print(f"Running: django-admin startproject {project_name}")
    subprocess.run(["django-admin", "startproject", project_name], check=True)
    target_dir = base_dir / project_name

    # Step 2: Create Django app
    subprocess.run(
        [sys.executable, str(target_dir / "manage.py"), "startapp", app_name],
        check=True,
    )

    # Step 3: Copy boilerplate templates
    # Access boilerplate inside the package using importlib.resources
    template_dir = Path(pkg_resources.files(__package__).joinpath("boilerplate"))
    render_and_copy(
        template_dir, target_dir, {"project_name": project_name, "app_name": app_name}
    )

    # Step 4: Initialize git if requested
    if args.git:
        subprocess.run(["git", "init"], cwd=target_dir, check=True)
        print("Initialized empty Git repository.")

    print(f"\n✅ Django project '{project_name}' is ready!")
    print(
        f"Next steps:\n  cd {project_name}\n  python -m venv venv && source venv/bin/activate"
    )
    print("  pip install -r requirements.txt")
    print("  python manage.py migrate\n  python manage.py runserver")
