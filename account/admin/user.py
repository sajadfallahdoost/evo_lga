from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'email', 'national_id', 'role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('phone_number', 'email', 'national_id')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'national_id', 'avatar_url')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'national_id', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'role'),
        }),
    )
    ordering = ['phone_number']
    readonly_fields = ('created_at', 'updated_at')
