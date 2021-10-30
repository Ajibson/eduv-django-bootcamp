from django.urls import path
from .views import blogs_posts, single_blog

app_name = "blog"

urlpatterns = [
    path("", blogs_posts.as_view(), name="blogs"),
    path("single_blog/<slug:blog_slug>", single_blog, name="single_blog")
]
