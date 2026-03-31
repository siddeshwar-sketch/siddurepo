from django.contrib import admin
from .models import Donation

class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'campaign', 'donor', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('campaign__title', 'donor__email', 'donor_name', 'donor_email')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Donation, DonationAdmin)
