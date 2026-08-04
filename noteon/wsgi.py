"""
WSGI config for noteon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noteon.settings')

application = get_wsgi_application()

# Run database migrations automatically when Vercel initializes the container
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Migration error: {e}")

# Vercel entrypoint alias
app = application