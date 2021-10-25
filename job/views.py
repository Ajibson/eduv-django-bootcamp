from django.shortcuts import render, redirect
from .forms import JobForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category
from account.models import recuiter


def jobs(request):

    return render(request, 'jobs/job_listing.html')


def job_details(request):

    return render(request, 'jobs/job_details.html')


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
