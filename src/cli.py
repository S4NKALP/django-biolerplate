import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from .features import (
        FEATURES,
        get_feature_dependencies,
        get_selected_features_config,
    )
except ImportError:
    from features import (
        FEATURES,
        get_feature_dependencies,
        get_selected_features_config,
    )

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


def select_features():
    """Interactive checkbox-style feature selection."""
    try:
        return select_features_inquirer()
    except ImportError:
        return select_features_simple()


def select_features_inquirer():
    """Advanced interactive selection using inquirer library."""
    import inquirer

    print("\n Django Boilerplate Feature Selection")
    print("=" * 50)

    # Prepare choices for inquirer
    choices = []
    for key, feature in FEATURES.items():
        choice_text = f"{feature.name}"
        if feature.dependencies:
            dep_names = [
                FEATURES[dep].name for dep in feature.dependencies if dep in FEATURES
            ]
            if dep_names:
                choice_text += f" (depends on: {', '.join(dep_names)})"
        choices.append((choice_text, key))

    # Add special options
    choices.extend(
        [
            ("Select All Features", "all"),
            ("Minimal Setup (No Features)", "none"),
        ]
    )

    questions = [
        inquirer.Checkbox(
            "features",
            message="Select features to include (use ↑↓ to navigate, SPACE to select, ENTER to confirm)",
            choices=choices,
            default=[],
        )
    ]

    answers = inquirer.prompt(questions)

    if not answers or not answers["features"]:
        selected_features = []
    elif "all" in answers["features"]:
        selected_features = list(FEATURES.keys())
    elif "none" in answers["features"]:
        selected_features = []
    else:
        selected_features = answers["features"]

    # Add dependencies
    all_selected = set()
    for feature in selected_features:
        all_selected.update(get_feature_dependencies(feature))

    print("\n✅ Feature Selection Summary:")
    print("=" * 40)
    if all_selected:
        print("Selected features:")
        for feature_name in all_selected:
            feature = FEATURES[feature_name]
            print(f"  • {feature.name}")
    else:
        print("Minimal setup (no extra features)")
    print()

    return list(all_selected)


def select_features_simple():
    """Simple interactive selection without external dependencies."""
    print("\n Django Boilerplate Feature Selection")
    print("=" * 60)
    print("Select features by entering their numbers (comma-separated)")
    print("Example: 1,3,5 or 1-3,5 or 'all' for all features")
    print("=" * 60)
    print()

    available_features = list(FEATURES.keys())
    selected_features = []

    # Display all features with checkboxes
    for i, (key, feature) in enumerate(FEATURES.items(), 1):
        print(f"{i:2d}. ☐ {feature.name}")
        print(f"     {feature.description}")
        if feature.dependencies:
            dep_names = [
                FEATURES[dep].name for dep in feature.dependencies if dep in FEATURES
            ]
            if dep_names:
                print(f"     Dependencies: {', '.join(dep_names)}")
        print()

    print("=" * 60)
    print("Options:")
    print("  • Enter numbers: 1,3,5")
    print("  • Enter ranges: 1-3,5")
    print("  • Enter 'all' for all features")
    print("  • Enter 'none' for minimal setup")
    print("  • Press Enter to skip (minimal setup)")
    print()

    while True:
        choice = input("Your selection: ").strip().lower()

        if not choice or choice == "none":
            selected_features = []
            break
        elif choice == "all":
            selected_features = available_features
            break
        else:
            try:
                # Parse the selection
                indices = set()
                for part in choice.split(","):
                    part = part.strip()
                    if "-" in part:
                        # Handle ranges like "1-3"
                        start, end = map(int, part.split("-"))
                        indices.update(range(start - 1, end))
                    else:
                        # Handle single numbers
                        indices.add(int(part) - 1)

                # Validate indices
                valid_indices = [i for i in indices if 0 <= i < len(available_features)]
                if not valid_indices:
                    print("❌ No valid selections. Please try again.")
                    continue

                selected_features = [available_features[i] for i in valid_indices]
                break

            except (ValueError, IndexError):
                print("❌ Invalid selection format. Please try again.")
                print("   Examples: 1,3,5 or 1-3,5 or all")
                continue

    # Add dependencies
    all_selected = set()
    for feature in selected_features:
        all_selected.update(get_feature_dependencies(feature))

    print("\n✅ Feature Selection Summary:")
    print("=" * 40)
    if all_selected:
        print("Selected features:")
        for feature_name in all_selected:
            feature = FEATURES[feature_name]
            print(f"  • {feature.name}")
    else:
        print("Minimal setup (no extra features)")
    print()

    return list(all_selected)


def render_and_copy(
    src: Path, dst: Path, replacements: dict, selected_features: list = None
):
    """Recursively copy files and replace placeholders."""
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        for child in src.iterdir():
            new_name = child.name.replace(
                "__PROJECT__", replacements["project_name"]
            ).replace("__APP__", replacements["app_name"])
            render_and_copy(child, dst / new_name, replacements, selected_features)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix.lower() in TEXT_EXTS or src.name in {"Dockerfile", ".gitignore"}:
            text = src.read_text(encoding="utf-8")
            text = text.replace("{{ project_name }}", replacements["project_name"])
            text = text.replace("{{ app_name }}", replacements["app_name"])

            # Add feature-specific replacements
            if selected_features:
                config = get_selected_features_config(selected_features)
                text = text.replace("{{ third_party_apps }}", str(config["apps"]))
                text = text.replace(
                    "{{ middleware }}", generate_middleware_code(config["middleware"])
                )
                text = text.replace(
                    "{{ feature_settings }}",
                    generate_feature_settings(config["settings"]),
                )
                text = text.replace(
                    "{{ production_settings }}",
                    generate_feature_settings(config["production_settings"]),
                )
                text = text.replace(
                    "{{ requirements }}", "\n".join(config["requirements"])
                )

            dst.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(src, dst)


def generate_middleware_code(middleware: list) -> str:
    """Generate Python code to add middleware to the MIDDLEWARE list."""
    if not middleware:
        return ""

    lines = []
    for mw in middleware:
        lines.append(f'    "{mw}",')

    return "\n".join(lines)


def generate_feature_settings(settings: dict) -> str:
    """Generate Python code for feature-specific settings."""
    if not settings:
        return ""

    lines = []
    for key, value in settings.items():
        if isinstance(value, dict):
            lines.append(f"{key} = {repr(value)}")
        elif isinstance(value, list):
            lines.append(f"{key} = {repr(value)}")
        elif isinstance(value, str) and value.startswith("_split_env_list"):
            lines.append(f"{key} = {value}")
        elif isinstance(value, str) and value.startswith("("):
            lines.append(f"{key} = {value}")
        elif isinstance(value, str) and value.startswith("os.environ"):
            lines.append(f"{key} = {value}")
        else:
            lines.append(f"{key} = {repr(value)}")

    return "\n".join(lines)


def run():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a Django project from a boilerplate with optional features."
    )
    parser.add_argument("--project", "-p", help="Django project name")
    parser.add_argument("--app", "-a", help="Default app name")
    parser.add_argument("--git", action="store_true", help="Initialize Git repo")
    parser.add_argument(
        "--features",
        "-f",
        nargs="+",
        help="Features to include (e.g., drf cors whitenoise)",
    )
    parser.add_argument(
        "--all-features", action="store_true", help="Include all features"
    )
    parser.add_argument(
        "--minimal",
        action="store_true",
        help="Create minimal Django project (no extra features)",
    )
    parser.add_argument(
        "--list-features",
        action="store_true",
        help="List all available features and exit",
    )
    args = parser.parse_args()

    # Handle list features command
    if args.list_features:
        print("\n🚀 Available Django Boilerplate Features:")
        print("=" * 50)
        for i, (key, feature) in enumerate(FEATURES.items(), 1):
            print(f"{i}. {feature.name} ({key})")
            print(f"   {feature.description}")
            if feature.dependencies:
                print(f"   Dependencies: {', '.join(feature.dependencies)}")
            print()
        return

    project_name = args.project or input("Enter your Django project name: ").strip()
    app_name = args.app or input("Enter your first Django app name: ").strip()

    if not valid_name(project_name) or not valid_name(app_name):
        print(
            "Project and app names must start with a letter and contain only letters, numbers, and underscores."
        )
        sys.exit(1)

    # Feature selection
    if args.minimal:
        selected_features = []
    elif args.all_features:
        selected_features = list(FEATURES.keys())
    elif args.features:
        selected_features = args.features
        # Validate features
        invalid_features = [f for f in selected_features if f not in FEATURES]
        if invalid_features:
            print(f"Invalid features: {', '.join(invalid_features)}")
            print(f"Available features: {', '.join(FEATURES.keys())}")
            sys.exit(1)
    else:
        selected_features = select_features()

    base_dir = Path.cwd()

    # Step 1: Create Django project
    print(f"\n📁 Creating Django project: {project_name}")
    subprocess.run(
        [sys.executable, "-m", "django", "startproject", project_name], check=True
    )

    target_dir = base_dir / project_name

    # Resolve template directory path (prefer packaged resources)
    try:
        import importlib.resources as resources  # Python 3.9+

        template_dir = Path(resources.files("boilerplate"))
    except Exception:
        template_dir = Path(__file__).parent / "boilerplate"

    # Decide whether to run startapp based on boilerplate contents
    boilerplate_app_exists = (template_dir / "__APP__").exists()

    # Step 2: Create Django app (only if boilerplate does not provide it)
    if not boilerplate_app_exists:
        print(f"📱 Creating Django app: {app_name}")
        subprocess.run(
            [sys.executable, str(target_dir / "manage.py"), "startapp", app_name],
            check=True,
        )

    # Remove default files first so boilerplate can replace them
    default_files_to_remove = [
        target_dir / project_name / "settings.py",
        target_dir / project_name / "asgi.py",
        target_dir / project_name / "wsgi.py",
    ]
    for path in default_files_to_remove:
        if path.exists():
            try:
                path.unlink()
            except Exception:
                pass

    # Step 3: Copy boilerplate templates with feature selection
    print(" Applying boilerplate templates...")

    if not template_dir.exists():
        print(f" Template directory not found: {template_dir}")
        print("Please ensure the boilerplate templates are available.")
        print(f"Current working directory: {Path.cwd()}")
        print(f"CLI file location: {Path(__file__).parent}")
        sys.exit(1)

    render_and_copy(
        template_dir,
        target_dir,
        {"project_name": project_name, "app_name": app_name},
        selected_features,
    )

    # Step 4: Initialize git if requested
    if args.git:
        subprocess.run(["git", "init"], cwd=target_dir, check=True)
        print(" Initialized empty Git repository.")

    print(f"\n Django project '{project_name}' is ready!")
    print(
        f" Selected features: {', '.join([FEATURES[f].name for f in selected_features]) if selected_features else 'None (minimal setup)'}"
    )
    print("\n Next steps:")
    print(f"  cd {project_name}")
    print("  python -m venv venv && source venv/bin/activate")
    print("  pip install -r requirements.txt")
    print("  python manage.py migrate")
    print("  python manage.py runserver")
