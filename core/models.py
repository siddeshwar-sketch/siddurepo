from django.db import models
from django.conf import settings
import uuid
import string
import random

class SupportTicket(models.Model):
    class Category(models.TextChoices):
        PAYMENT = 'PAYMENT', 'Payment Issue'
        VERIFICATION = 'VERIFICATION', 'Verification Help'
        ACCOUNT = 'ACCOUNT', 'Account Problems'
        OTHER = 'OTHER', 'Other / General'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_tickets')
    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    admin_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            # Generate a unique ID like TKT-7X3A2
            random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            self.ticket_id = f"TKT-{random_chars}"
            
            # Ensure uniqueness
            while SupportTicket.objects.filter(ticket_id=self.ticket_id).exists():
                random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                self.ticket_id = f"TKT-{random_chars}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
