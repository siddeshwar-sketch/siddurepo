from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='categories/icons/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Campaign(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending Approval')
        DRAFT = 'DRAFT', _('Draft')
        ACTIVE = 'ACTIVE', _('Active')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')
        REJECTED = 'REJECTED', _('Rejected')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='campaigns/images/', null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='campaigns')
    location = models.CharField(max_length=255, blank=True)
    
    payment_qr_code = models.ImageField(upload_to='campaigns/qr_codes/', null=True, blank=True, help_text="Upload your UPI or Bank QR code here")
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    approved = models.BooleanField(default=False)
    status_reason = models.TextField(blank=True, null=True, help_text="Reason for current status or rejection notes")
    amount_issued = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Total amount paid out to the seeker")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def progress_percentage(self):
        if self.goal_amount > 0:
            return round((self.raised_amount / self.goal_amount) * 100, 2)
        return 0

    @property
    def is_funded(self):
        return self.raised_amount >= self.goal_amount

class CampaignProof(models.Model):
    class DocumentType(models.TextChoices):
        IDENTITY = 'IDENTITY', _('Identity Proof')
        MEDICAL = 'MEDICAL', _('Medical Document')
        FINANCIAL = 'FINANCIAL', _('Financial Estimate')
        OTHER = 'OTHER', _('Other')

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='proofs')
    document = models.FileField(upload_to='campaigns/proofs/')
    document_type = models.CharField(max_length=20, choices=DocumentType.choices, default=DocumentType.OTHER)
    description = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.campaign.title}"
