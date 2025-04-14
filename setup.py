import os
import subprocess
import sys
from setuptools import setup, find_packages

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e)
        sys.exit(1)

def main():
    # Create Django project
    run_command("django-admin startproject reddit_clone .")
    
    # Create apps
    apps = ["users", "subreddits", "posts"]
    for app in apps:
        run_command(f"python manage.py startapp {app}")
    
    # Create necessary directories
    directories = [
        "static",
        "templates",
        "media",
        "templates/base",
        "templates/users",
        "templates/subreddits",
        "templates/posts"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Project structure created successfully!")
    print("Next steps:")
    print("1. Create a virtual environment and install requirements")
    print("2. Run migrations")
    print("3. Create a superuser")
    print("4. Start the development server")

setup(
    name="redditClone",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "Django==5.0.2",
        "Pillow==10.2.0",
        "django-crispy-forms==2.1",
        "crispy-tailwind==0.5.0",
        "django-allauth==0.60.1",
        "python-dotenv==1.0.1",
        "django-environ==0.11.2",
        "psycopg2-binary==2.9.9",
        "dj-database-url==2.1.0",
        "gunicorn",
        "whitenoise",
        "crispy_bootstrap5",
        "django-bootstrap5",
    ],
)

if __name__ == "__main__":
    main() 