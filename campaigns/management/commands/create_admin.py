"""
Management command to create the default superadmin user.
Safe to run multiple times — uses get_or_create.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates the default admin user if it does not already exist.'

    def handle(self, *args, **kwargs):
        email = os.environ.get('ADMIN_EMAIL', 'sharanprakashpatil70558@gmail.com')
        password = os.environ.get('ADMIN_PASSWORD', 'sharan@1234')
        username = 'admin'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            }
        )

        # Always update email and ensure superuser rights
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Admin user already exists, password updated: {email}'))
