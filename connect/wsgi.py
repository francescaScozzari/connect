"""
WSGI config for Connect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_CONFIGURATION", "Remote")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connect.settings")

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
