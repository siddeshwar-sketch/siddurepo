import os
import django
from django.conf import settings
from django.core.mail import send_mail

# Force the settings module just like in manage.py default (local)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

print("--- Testing SMTP Settings ---")
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"User: {settings.EMAIL_HOST_USER}")
# Don't print password for safety, but check it
print(f"Password set: {bool(settings.EMAIL_HOST_PASSWORD)}")
print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")

try:
    print("\nSending test email...")
    send_mail(
        'Platform SMTP Test',
        'If you see this, your SMTP settings are working perfectly!',
        settings.DEFAULT_FROM_EMAIL,
        ['sharanprakashpatil70558@gmail.com'], # Sending to himself
        fail_silently=False,
    )
    print("SUCCESS: Email sent!")
except Exception as e:
    print(f"FAILED: {e}")
