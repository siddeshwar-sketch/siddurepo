from django.contrib import admin
from .models import SupportTicket

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'user', 'subject', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('ticket_id', 'subject', 'message', 'user__username', 'user__email')
    readonly_fields = ('ticket_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Info', {
            'fields': ('ticket_id', 'user', 'created_at', 'updated_at')
        }),
        ('Content', {
            'fields': ('subject', 'category', 'message')
        }),
        ('Resolution', {
            'fields': ('status', 'admin_notes')
        }),
    )
