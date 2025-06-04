import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User

username = "admin"
password = "admin"

if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists.")
else:
    User.objects.create_user(username=username, password=password)
    print(f"User '{username}' created with password '{password}'.")
