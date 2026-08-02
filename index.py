import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noteon.settings')

app = get_wsgi_application()

# Run database migrations in Vercel's temporary /tmp folder on startup
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Migration error: {e}")