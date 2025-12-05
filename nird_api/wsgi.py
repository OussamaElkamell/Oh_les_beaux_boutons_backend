"""
WSGI config for nird_api project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nird_api.settings')

application = get_wsgi_application()
