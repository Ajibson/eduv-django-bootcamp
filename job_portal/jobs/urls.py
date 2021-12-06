from django.urls import path
from .views import job_listing, post_job

app_name = "jobs"

urlpatterns = [
    path("jobs-listing/", job_listing, name="job_listing"),
    path("post-job/", post_job, name="post_job")
]
