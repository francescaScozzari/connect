"""
ASGI config for Connect project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os

os.environ.setdefault("DJANGO_CONFIGURATION", "Remote")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connect.settings")

from configurations.asgi import get_asgi_application

application = get_asgi_application()
