from django.db import models
from django.conf import settings
from campaigns.models import Campaign
from django.utils.translation import gettext_lazy as _

class Donation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        SUCCESS = 'SUCCESS', _('Success')
        FAILED = 'FAILED', _('Failed')

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='donations')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    donor_name = models.CharField(max_length=255, blank=True)
    donor_email = models.EmailField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    payment_id = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Donation {self.id} - {self.campaign.title} - {self.amount}"
