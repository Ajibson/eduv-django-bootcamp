from django.shortcuts import render, redirect
from .forms import JobForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Job
from account.models import recuiter
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage


def jobs(request):
    if request.method == "POST":
        gotten_category = request.POST.get('selected_category')
        data = {}
        new_data = Job.objects.filter(category=gotten_category).values()
        # data['response'] = new_data.values()
        # print(data)
        return JsonResponse({"response": list(new_data)})
    # Get the list tto paginate
    available_jobs = Job.objects.order_by("-date_created")
    paginator = Paginator(available_jobs, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    context = {"page_obj": page_obj, "jobs_found": len(
        available_jobs), "categories": categories}
    return render(request, 'jobs/job_listing.html', context)


def job_details(request, job_slug, company):
    posted_by = recuiter.objects.filter(company_name=company).first()
    the_job = Job.objects.filter(
        job_slug=job_slug, posted_by=posted_by).first()
    knowledge_skill = the_job.Knowledge_skills_abilities.split(',')

    education_experience = the_job.education_experience.split(',')

    context = {
        'the_job': the_job, "posted_by": posted_by, "knowledge_skill": knowledge_skill,
        "education_experience": education_experience
    }
    return render(request, 'jobs/job_details.html', context)


@login_required()
def new_job(request):
    if request.user.status == "job_seeker":
        messages.error(request, "You are not permitted to post jobs")
        return redirect("account:index")
    elif not recuiter.objects.get(user=request.user).cleared:
        messages.error(
            request, "You are not cleared yet to post jobs, Please contact the admin")
        return redirect("account:index")
    else:
        categories = Category.objects.all()
        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Job posted successfully")
                return redirect("account:index")
            else:
                return render(request, 'jobs/job.html', {"form": form, "categories": categories})

        form = JobForm()
        return render(request, 'jobs/job.html', {"form": form, "categories": categories})
