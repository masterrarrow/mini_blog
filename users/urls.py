from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import (
    SignUpView, activate, LoginView, UserProfileView,
    UserDeleteView, PasswordResetRequestView)
from django.conf.urls import url


app_name = "user"


urlpatterns = [
    # User registration and account activation
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    # Login and logout
    path('sign-in/', LoginView.as_view(), name='sign-in'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # User profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    # Delete user
    path('delete/<int:pk>/user/', UserDeleteView.as_view(), name='user-delete'),
    # Request a user password reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
]
