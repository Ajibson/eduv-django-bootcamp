from django.urls import path
from .views import (index, about, contact, signup, Login,
                    password_reset, account_confirmation)

app_name = "account"

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path('contact/', contact, name="contact"),

    # authentication urls
    path('signup/', signup, name="signup"),
    path("activate/<uidb64>/<token>/", account_confirmation,
         name="account-confirmation"),
    path("login/", Login, name="login"),
    path("password-reset/", password_reset, name="password-reset")
]
