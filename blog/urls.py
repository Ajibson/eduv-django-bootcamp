from django.urls import path
from .views import blogs, single_blog

app_name = "blog"

urlpatterns = [
    path("", blogs, name="blogs"),
    path("single_blog/", single_blog, name = "single_blog")
]
