from django.urls import path
from .views import jobs, job_details, new_job, job_filter

app_name = "jobs"

urlpatterns = [
    path("", jobs, name="jobs-listing"),
    path('<str:company>/<str:job_slug>', job_details, name="job-details"),
    path("new-job/", new_job, name="new-job"),
    path("job_filter/", job_filter, name="job_filter")
]
