"""
WSGI config for tasktopia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tasktopia.settings')

# Create the WSGI application callable
try:
    application = get_wsgi_application()
except Exception as e:
    print("Exception occurred while getting WSGI application:", e)
    raise
