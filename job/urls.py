from django.urls import path
from .views import jobs, job_details

app_name = "jobs"

urlpatterns = [
    path("", jobs, name="jobs-listing"),
    path('job-details/', job_details, name = "job-details")
]
