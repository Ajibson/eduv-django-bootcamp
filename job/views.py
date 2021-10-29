from django.shortcuts import render, redirect
from .forms import JobForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Job, JobNatureOption
from account.models import recuiter
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core import serializers
from django.template.loader import render_to_string
from django.db.models import Q


def get_job(gotten_category=None, job_nature=None, minamount=None, maxamount=None):
    query = Q()
    # If all filter seen
    if gotten_category != None and job_nature and minamount != None and maxamount != None:
        for word in job_nature:
            query = query | Q(job_nature=word) & Q(
                category=gotten_category) & Q(salary_range__gte=minamount) & Q(salary_range__lte=maxamount)
        available_jobs = Job.objects.filter(
            query).distinct().order_by("-date_created")

    # If category and job_nature seen
    elif gotten_category != None and job_nature:
        for word in job_nature:
            query = query | Q(job_nature=word) & Q(
                category=gotten_category)
        available_jobs = Job.objects.filter(
            query).distinct().order_by("-date_created")
    # If price and either category or job_ature seen
    elif (gotten_category != None or job_nature) and minamount != None and maxamount != None:
        # price with category
        if gotten_category != None:
            query = query | Q(
                category=gotten_category) & Q(salary_range__gte=minamount) & Q(salary_range__lte=maxamount)
            available_jobs = Job.objects.filter(
                query).distinct().order_by("-date_created")
        # price with job_nature
        else:
            for word in job_nature:
                query = query | Q(job_nature=word) & Q(
                    salary_range__gte=minamount) & Q(salary_range__lte=maxamount)
            available_jobs = Job.objects.filter(
                query).distinct().order_by("-date_created")
    # category alone
    elif gotten_category != None:
        available_jobs = Job.objects.filter(
            category=gotten_category).order_by("-date_created")
    # job_nature alone
    elif job_nature:
        for word in job_nature:
            query = query | Q(job_nature=word)
        available_jobs = Job.objects.filter(
            query).distinct().order_by("-date_created")
    elif minamount != None and maxamount != None:
        query = query | Q(salary_range__gte=minamount) & Q(
            salary_range__lte=maxamount)
        available_jobs = Job.objects.filter(
            query).distinct().order_by("-date_created")
    else:
        available_jobs = Job.objects.order_by("-date_created")
    return available_jobs


def job_filter(request):
    gotten_category = request.POST.get('selected_category')
    job_nature = request.POST.getlist("job_nature[]")
    minamount = request.POST.get("minamount")
    maxamount = request.POST.get("maxamount")
    available_jobs = get_job(gotten_category, job_nature, minamount, maxamount)
    categories = Category.objects.all()
    paginator = Paginator(available_jobs, 2)
    page_number = request.POST.get('page', 1)
    page_obj = paginator.get_page(page_number)
    data = {
        "page_obj": page_obj, "jobs_found": len(
            available_jobs), "categories": categories
    }
    job_listing_to_string = render_to_string("jobs/job_filter.html", data)
    pagination_to_string = render_to_string(
        'jobs/pagination.html', {"page_obj": page_obj})
    return JsonResponse({"jobs": job_listing_to_string, "pagination": pagination_to_string})


def jobs(request):
    available_jobs = Job.objects.order_by("-date_created")
    paginator = Paginator(available_jobs, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    context = {"page_obj": page_obj, "jobs_found": len(
        available_jobs), "categories": categories, "job_nature": JobNatureOption.choices}
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
