# support/urls.py
from django.urls import path
from support.api.views import notification_title, notification_detail, comment_detail, comment_title, ticket_detail, ticket_title


urlpatterns = [
    path('tickets/', notification_title, name='tickets-list'),
    path('tickets/', ticket_title, name='ticket-detail'),
    path('tickets/<int:pk>/', ticket_detail, name='ticket-detail'),

    path('comments/', comment_title, name='comment-list'),
    path('comments/<int:pk>/', comment_detail, name='comment-detail'),

    path('notifications/', notification_title, name='notification-list'),
    path('notifications/<int:pk>/', notification_detail, name='notification-detail'),
]
