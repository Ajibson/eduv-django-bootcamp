import django
from django.urls import path
from .views import signup, Login, Logout, confirm_email_view, get_token
from django.http import HttpResponse
app_name = "account"


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", Login, name="login"),
    path("logout/", Logout, name="logout"),
    path("confirm-email/<uidb64>/<token>/",
         confirm_email_view, name="confirm_email"),
    path("get-token/", get_token, name = "token")
    # path('users/<str:email>', show),
]
