"""
WSGI config for geobin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Load environment variables FIRST, before Django setup
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geobin.settings')

application = get_wsgi_application()
