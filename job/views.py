from django.shortcuts import render


def jobs(request):

    return render(request, 'jobs/job_listing.html')


def job_details(request):

    return render(request, 'jobs/job_details.html')
