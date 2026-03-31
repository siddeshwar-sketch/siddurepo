from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'verified', 'is_staff')
    list_filter = ('role', 'verified', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('role', 'profile_image', 'verified', 'phone_number', 'otp_code', 'otp_expiry')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile', {'fields': ('role', 'profile_image', 'verified', 'phone_number')}),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
