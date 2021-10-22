from django.urls import path
from .views import blogs

app_name = "blog"

urlpatterns = [
    path("", blogs, name="blogs"),
]
