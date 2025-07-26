#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Load environment variables FIRST, before anything else
try:
    from dotenv import load_dotenv
    # Try multiple paths to find the .env file
    env_paths = [
        '.env',
        '/usr/src/app/.env',
        os.path.join(os.path.dirname(__file__), '.env')
    ]
    
    env_loaded = False
    for env_path in env_paths:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"Environment file loaded from: {env_path}")
            env_loaded = True
            break
    
    if not env_loaded:
        print("No .env file found in any of these paths:")
        for path in env_paths:
            print(f"  - {path} (exists: {os.path.exists(path)})")
    
    # Debug: Print some environment variables (safely)
    print(f"DB_HOST is set: {'Yes' if os.environ.get('DB_HOST') else 'No'}")
    
except ImportError:
    print("python-dotenv not installed, skipping .env loading")
except Exception as e:
    print(f"Error loading .env file: {e}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geobin.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()