from django.db import models
from django.utils.translation import gettext_lazy as _
from donations.models import Donation

class Transaction(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
        REFUNDED = 'REFUNDED', _('Refunded')

    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='transaction')
    gateway_response = models.JSONField(default=dict, blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED
    )
    
    stripe_charge_id = models.CharField(max_length=255, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    
    razorpay_order_id = models.CharField(max_length=255, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True)
    razorpay_signature = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction for {self.donation} - {self.verification_status}"
