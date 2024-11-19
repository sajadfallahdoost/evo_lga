from django.urls import path
from account.api.views import user_profile, change_password, register_or_login_user, user_profile_by_id

urlpatterns = [
    path('register_or_login_user/', register_or_login_user, name='register_or_login_user'),
    path('user-profile/<int:user_id>/', user_profile_by_id, name='user-profile-by-id'),
    path('profile/', user_profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
]
