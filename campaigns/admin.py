from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Category, Campaign, CampaignProof


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class CampaignProofInline(admin.TabularInline):
    model = CampaignProof
    extra = 0


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'goal_amount', 'status', 'approved', 'review_note')
    list_filter = ('status', 'approved', 'category', 'created_at')
    search_fields = ('title', 'description', 'owner__username', 'owner__email', 'location')
    list_editable = ('status', 'approved')
    readonly_fields = ('owner', 'created_at', 'updated_at', 'raised_amount', 'amount_issued')
    inlines = [CampaignProofInline]
    actions = ['approve_campaigns', 'reject_campaigns', 'mark_pending_review']
    fieldsets = (
        ('Campaign Request', {
            'fields': ('title', 'owner', 'category', 'description', 'goal_amount', 'location', 'image')
        }),
        ('Review Decision', {
            'fields': ('status', 'approved', 'status_reason')
        }),
        ('Funding Summary', {
            'fields': ('raised_amount', 'amount_issued', 'payment_qr_code', 'bank_name', 'bank_account_number', 'ifsc_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description='Admin review')
    def review_note(self, obj):
        if obj.status == Campaign.Status.ACTIVE:
            return format_html('<span style="color: #15803d; font-weight: 600;">Accepted</span>')
        if obj.status == Campaign.Status.REJECTED:
            reason = obj.status_reason or 'Rejected by admin.'
            return format_html('<span style="color: #b91c1c; font-weight: 600;">Rejected</span><br><small>{}</small>', reason)
        return format_html('<span style="color: #b45309; font-weight: 600;">Pending review</span>')

    @admin.action(description='Accept selected campaign requests')
    def approve_campaigns(self, request, queryset):
        updated = queryset.update(approved=True, status=Campaign.Status.ACTIVE, status_reason='')
        self.message_user(request, f'{updated} campaign request(s) accepted.', level=messages.SUCCESS)

    @admin.action(description='Reject selected campaign requests')
    def reject_campaigns(self, request, queryset):
        updated = queryset.update(
            approved=False,
            status=Campaign.Status.REJECTED,
            status_reason='Rejected by admin.',
        )
        self.message_user(request, f'{updated} campaign request(s) rejected.', level=messages.WARNING)

    @admin.action(description='Move selected campaign requests back to pending review')
    def mark_pending_review(self, request, queryset):
        updated = queryset.update(approved=False, status=Campaign.Status.PENDING)
        self.message_user(request, f'{updated} campaign request(s) marked as pending.', level=messages.INFO)


@admin.register(CampaignProof)
class CampaignProofAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'document_type', 'is_verified')
    list_filter = ('is_verified', 'document_type')
    list_editable = ('is_verified',)
