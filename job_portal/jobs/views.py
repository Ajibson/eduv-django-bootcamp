from django.shortcuts import render, redirect
from .job_forms import JobForm
from .models import jobs, Category
from django.contrib import messages
from account.models import recruiter
from django.contrib.auth.decorators import login_required


def job_listing(request):

    return render(request, "jobs/job_listing.html")


@login_required()
def post_job(request):
    gotten_categories = Category.objects.all()
    if request.method == "POST":
        if request.user.status == "recuiter":
            form = JobForm(request.POST)
            if form.is_valid():
                new_job_form = form.save(commit=False)
                new_job_form.posted_by = recruiter.objects.get(user=request.user)
                new_job_form.save()
                messages.success(request, "Job posted successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid form submission")
                context = {"categories": gotten_categories, "form": form}
                return render(request, "jobs/job.html", context=context)
        else:
            messages.error(request, "You are not permitted to post a job")
            return redirect("jobs:post_job")
    context = {"categories": gotten_categories}
    return render(request, "jobs/job.html", context=context)


def job_detail(request, company_name, job_title, id):
    job_recruiter = recruiter.objects.get(company_name=company_name)
    the_job = jobs.objects.get(posted_by=job_recruiter, title=job_title, id=id)
    requirements = the_job.requirements.split(",")
    education_experience = the_job.education_experience.split(",")
    context = {
        "job": the_job,
        "requirements": requirements,
        "education_experience": education_experience,
    }

    return render(request, "jobs/job_details.html", context)
