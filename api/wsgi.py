"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)  # Add logger instance

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

logger.info("wsgi")

app = get_wsgi_application()
