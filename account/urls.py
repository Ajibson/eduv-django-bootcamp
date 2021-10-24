from django.urls import path
from .views import (index, about, contact, signup, Login, Logout, password_reset_complete,
                    password_reset, account_confirmation, update_account)
from django.contrib.auth import views as auth_views
app_name = "account"

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path('contact/', contact, name="contact"),

    # authentication urls
    path('signup/', signup, name="signup"),
    path("activate/<uidb64>/<token>/", account_confirmation,
         name="account-confirmation"),
    path('update-account', update_account, name="update-account"),
    path("login/", Login, name="login"),
    path("ogout/", Logout, name="logout"),
    path("password-reset/", password_reset, name="password-reset"),
    # path("password_reset_done", password_reset_done, name = "password_reset_done"),
    # path("password_reset_confirm/<uidb64>/<token>/",
    #      password_reset_confirm, name="password_reset_confirm")

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/email_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', password_reset_complete,
         name='password_reset_complete'),
]
