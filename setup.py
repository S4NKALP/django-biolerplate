from setuptools import find_packages, setup


# Read the README file for long description
def read_readme():
    """Read the README file."""
    try:
        with open("readme.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "A CLI tool to set up Django projects with modern structure and best practices."


setup(
    name="django-init",
    version="0.1.0",
    description="A CLI tool to set up Django projects with modern structure and best practices.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Sankalp Tharu",
    author_email="sankalptharu50028@gmail.com",
    url="https://github.com/S4NKALP/django-init",
    packages=find_packages(include=["cli", "cli.*"]),
    include_package_data=True,
    install_requires=[
        "black>=24.10.0",
        "click>=8.1.8",
        "rich>=13.9.4",
    ],
    entry_points={
        "console_scripts": [
            "django-init=cli.script:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "Django",
        "CLI",
        "Project Setup",
    ],
    python_requires=">=3.11",
    project_urls={
        "Bug Reports": "https://github.com/S4NKALP/django-init/issues",
        "Source": "https://github.com/S4NKALP/django-init",
        "Documentation": "https://github.com/S4NKALP/django-init#readme",
    },
)
