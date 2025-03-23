# backend/quanlydaily/asgi.py
"""
ASGI config for quanlydaily project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quanlydaily.settings')

application = get_asgi_application()