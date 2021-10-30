from django.shortcuts import render, redirect

from account.models import Account, job_seeker, recuiter, passwordresetcode
from .forms import SignUpForm, job_seekerForm, CompanyForm, LoginForm, NewPasswordResetForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .email import new_recuiter
from blog.models import blogs

from job.models import Category, Job


def index(request):
    categories = Category.objects.all()
    cat_dict = {}
    new_blogs = blogs.objects.filter(
        status="Published").order_by("-date_published")
    for category in categories:
        job_categories = Job.objects.filter(category=category.name)
        cat_dict[category] = len(job_categories)
    hot_jobs = Job.objects.order_by("-date_created")[:3]
    job_seekers = len(job_seeker.objects.all())
    recuiters = len(recuiter.objects.all())
    context = {
        'cat_dict': cat_dict, "hot_jobs": hot_jobs, "job_seekers": job_seekers, "recuiters": recuiters, "new_blogs": new_blogs[:3]
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.set_password(form.cleaned_data.get("password"))
            new_account.save()
            messages.success(
                request, "Registration Successfully, Head over to your email to verify your account")
            return redirect("account:index")
        else:
            return render(request, 'account/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def Login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user and user.is_verified:
                login(request, user)

                return redirect(request.GET.get("next", '/'))
            elif user and not user.is_verified:
                messages.error(
                    request, "Please confirm your email through the mail sent to you on registration")
                return redirect('account:login')
            else:
                messages.error(request, "Wrong credentials supplied")
                return render(request, 'account/login.html')
        else:
            messages.error(request, "what are you putting in the form 😎")
            return redirect("account:login")
    return render(request, 'account/login.html')


def Logout(request):
    logout(request)
    messages.success(request, "We hope to see you back very soon")
    return redirect("account:index")


def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Account.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    token = default_token_generator.make_token(user)
                    password_token = passwordresetcode.objects.filter(
                        user=user)
                    password_token.delete()

                    # Create new password reset token
                    stored_token = passwordresetcode.objects.create(
                        code=token, user=user)
                    subject = "Password Reset Link"
                    email_template_name = "account/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'http://eduvjobs.herokuapp.com',
                        'site_name': 'Eduv Job Portal',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': token,
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'helpraisemyfund@gmail.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return render(request, 'account/email_sent.html')
    password_reset_form = PasswordResetForm()
    return render(request, 'account/password_reset.html', context={"password_reset_form": password_reset_form})


def password_reset_confirm(request, uidb64, token):
    user_pk = force_text(urlsafe_base64_decode(uidb64))
    try:
        user = Account.objects.get(pk=user_pk)
        get_token = passwordresetcode.objects.get(code=token)
        if request.method == 'POST':
            form = NewPasswordResetForm(request.POST)
            if form.is_valid():
                get_token.delete()
                password = form.cleaned_data['confirm_password']
                user.set_password(password)
                user.save()
                messages.success(request, "Password set successfully")
                return redirect('account:login')
            else:
                return render(request, 'account/password_confirm.html', {'form': form})
        else:
            date = timezone.now() - get_token.created_at
            if date.seconds > 3600:  # 60 min set for link expiration
                get_token.delete()
                messages.error(request, "Reset link has expired")
                return redirect('account:password-reset')
            else:
                form = NewPasswordResetForm()
                return render(request, 'account/password_confirm.html', {'form': form})
    except (Account.DoesNotExist, passwordresetcode.DoesNotExist):
        messages.error(
            request, "Reset link has been revoked, Kindly request for another")
        return redirect('account:password-reset')


def password_reset_complete(request):
    return redirect("account:login")


def account_confirmation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None:
        user.is_verified = True
        user.save()
        if user.status == "job_seeker":
            form = job_seekerForm()
            login(request, user)
            return render(request, 'account/job_seeker.html', {'form': form})
        elif user.status == 'recuiter':
            form = CompanyForm()
            login(request, user)
            return render(request, 'account/recuiter.html', {'form': form})
    else:
        # invalid link
        messages.error(request, "Invalid Link")
        form = SignUpForm()
        return render(request, 'account/signup.html', {'form': form})


@login_required()
def update_account(request):
    status = request.GET.get("status")
    if request.method == 'POST':
        if request.user.status == "job_seeker":
            instance = job_seeker.objects.filter(user=request.user).first()
            form = job_seekerForm(
                request.POST, request.FILES, instance=instance)
        else:
            instance = recuiter.objects.filter(user=request.user).first()
            form = CompanyForm(
                request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if status == "new":
                send_message = new_recuiter(
                    recuiter.objects.filter(user=request.user).first())
            messages.success(request, "Account Updated Successfully")
            return redirect("account:index")
        else:
            messages.error(request, f"Resume {form.errors['resume'][0]}")
            return redirect(request.META.get('HTTP_REFERER', '/'))
    if request.user.status == "job_seeker":
        instance = job_seeker.objects.filter(user=request.user).first()
        form = job_seekerForm(instance=instance)
        return render(request, 'account/job_seeker.html', {"form": form})
    else:
        instance = recuiter.objects.filter(user=request.user).first()
        form = CompanyForm(instance=instance)
        return render(request, 'account/recuiter.html', {"form": form, 'status': status})


def clear_recuiter(request):
    pk = request.GET.get("pk")
    recuiter_to_clear = recuiter.objects.filter(pk=pk).first()
    if recuiter_to_clear:
        recuiter_to_clear.cleared = True
        recuiter_to_clear.save()
        messages.success(request, "Recuiter cleared successfully")
        return redirect("account:index")
    else:
        messages.error(request, "Recuiter not Found")
        return redirect("account:index")
