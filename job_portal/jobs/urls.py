from django.urls import path
from .views import job_listing, post_job,job_detail

app_name = "jobs"

urlpatterns = [
    path("jobs-listing/", job_listing, name="job_listing"),
    path("post-job/", post_job, name="post_job"),
    path("jobs/<str:company_name>/<str:job_title>/<int:id>/", job_detail, name = "job_details"),
]
