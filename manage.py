#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Load environment variables FIRST, before anything else
try:
    from dotenv import load_dotenv
    # Explicitly specify the .env file path
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    print("Environment file loaded successfully")  # Debug line
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