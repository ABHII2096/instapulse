"""
WSGI config for insta project.
"""

import os
from django.core.wsgi import get_wsgi_application

# ✅ MUST point to insta/settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insta.settings')

application = get_wsgi_application()

