import os
import sys

import django
from django.contrib.auth import get_user_model

sys.path.append('/code')

django.setup()

username = os.environ['DJANGO_SUPERUSER_NAME']
email = os.environ['DJANGO_SUPERUSER_EMAIL']
password = os.environ['DJANGO_SUPERUSER_PASSWORD']

User = get_user_model()

try:
    admin = User.objects.get(username=username)
    admin.set_password(password)
    admin.email = email
    admin.save()
except User.DoesNotExist:
    admin = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
