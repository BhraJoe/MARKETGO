import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketgo.settings')

from marketgo.wsgi import application

if os.getenv('VERCEL'):
	from django.core.management import call_command

	call_command('migrate', '--noinput', verbosity=0)

app = application
