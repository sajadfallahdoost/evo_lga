# support/admin.py
from django.contrib import admin
from support.models import Ticket, Comment, Notification


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'assigned_to', 'priority', 'status', 
                    'created_at')
    list_filter = ('priority', 'status')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'message', 'created_at')
    search_fields = ('ticket__title', 'user__username', 'message')
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    readonly_fields = ('created_at',)
