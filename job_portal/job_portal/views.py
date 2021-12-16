from django.http import HttpResponse
from django.shortcuts import render
from jobs.models import jobs, Category
from account.models import job_seeker


def index(request):
    jobs_gotten = jobs.objects.all()
    categories = Category.objects.all()
    job_seekers_num = job_seeker.objects.all().count()
    cat_dict = {}
    # create a zip of category and number od job
    for cat in categories:
        job_related = jobs.objects.filter(category=cat).count()
        cat_dict[cat] = job_related

    context = {
        "jobs": jobs_gotten[:4],
        "job_seekers_num": job_seekers_num,
        "cat_dict": cat_dict,
    }
    return render(request, "index.html", context=context)
