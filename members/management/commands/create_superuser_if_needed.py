# members/management/commands/create_superuser_if_needed.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist and environment variables are set.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not User.objects.filter(username=username).exists():
            if username and email and password:
                self.stdout.write(f'Creating superuser: {username}')
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully.'))
            else:
                self.stdout.write('Superuser environment variables not set, skipping creation.')
        else:
            self.stdout.write(f'Superuser {username} already exists, skipping creation.')