from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'donation', 'verification_status', 'created_at')
    list_filter = ('verification_status', 'created_at')
    search_fields = ('donation__campaign__title', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('gateway_response', 'created_at', 'updated_at')

admin.site.register(Transaction, TransactionAdmin)
