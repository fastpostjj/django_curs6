from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from user_auth.apps import UserAuthConfig
from user_auth.views import UserForgotPasswordView, UserRegisterView, \
    ProfileUpdateView, RegisterView, generate_new_password, foggot_password, reset_password, \
    UserPasswordResetConfirmView, EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmedView, \
    EmailConfirmationFailedView, UsersListView, UserDetailView, UsersDraftListView, Toggle_Activity_User, \
    BlockedLoginView, blocked_page

app_name = UserAuthConfig.name

urlpatterns = [
    # path('', LoginView.as_view(template_name='user_auth/login.html'), name='login'),
    path('', BlockedLoginView.as_view(template_name='user_auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('blocked_page/', blocked_page, name='blocked_page'),

    path('users/', UsersListView.as_view(), name='users'),
    path('users_drafts/', UsersDraftListView.as_view(), name='users_drafts'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user'),
    path('user/toggle/<int:pk>/', Toggle_Activity_User.as_view(), name='toggle_activity_user'),

    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('profile/genpassword', generate_new_password, name='generate_new_password'),
    path('profile/foggotpassword', foggot_password, name='foggot_password'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('reset_password/', reset_password, name='reset_password'),
    ]

