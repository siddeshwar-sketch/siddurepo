from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        DONOR = 'DONOR', _('Donor')
        CAMPAIGN_OWNER = 'OWNER', _('Campaign Owner')
        ADMIN = 'ADMIN', _('Admin')

    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=15, unique=True, null=True, blank=True)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.DONOR
    )
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_donor(self):
        return self.role == self.Role.DONOR
    
    def is_campaign_owner(self):
        return self.role == self.Role.CAMPAIGN_OWNER
    
    def is_admin_role(self):
        return self.role == self.Role.ADMIN
