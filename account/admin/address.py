from django.contrib import admin
from account.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'state', 'postal_code', 'country', 'is_default')
    search_fields = ('user__email', 'address_line1', 'city', 'postal_code', 'country')
    list_filter = ('is_default', 'country')
    ordering = ['user']
