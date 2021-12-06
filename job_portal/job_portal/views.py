from django.http import HttpResponse
from django.shortcuts import render
from jobs.models import jobs


def index(request):
    job_gotten = jobs.objects.all()[:4]

    context = {
        "jobs": job_gotten
    }
    return render(request, "index.html", context=context)
