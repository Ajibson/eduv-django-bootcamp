from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from .models import User, confirmation_email
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .email import account_confirmation_email
from django.utils.http import urlsafe_base64_decode
from django.utils import timezone


def confirm_email_view(request, uidb64, token):
    # Decode the uidb64
    user_id = force_text(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(pk=user_id)
        db_token = confirmation_email.objects.get(token=token)
        time_diff = timezone.now() - db_token.created_at
        if time_diff.hours < 1:
            user.is_verified = True
            user.save()
            db_token.delete()
            messages.success(request, "Email confirmed successfully")
            return redirect("/")
        else:
            db_token.delete()
            messages.error(request, "Confirmation link expired")
            return redirect("account:token")

    except User.DoesNotExist:
        messages.error(request, "Please you need to register")
        return redirect("account:signup")
    except confirmation_email.DoesNotExist:
        messages.error(request, "Sorry token is invalid")
        return redirect("account:token")


def get_token(request):
    if request.method == "POST":
        try:
            email = request.POST['email']
            user = User.objects.get(email=email)
            # Send a confirmation email to user
            send_confirmation_email = account_confirmation_email(request, user)
            return redirect("/")
        except User.DoesNotExist:
            messages.error(
                request, "A confirmation link has been sent if the email exist in our database")
            return redirect("account:token")
    return render(request, 'accounts/token.html')


def signup(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.set_password(form.cleaned_data['password'])
            new_form.save()
            # Send a confirmation email to user
            send_confirmation_email = account_confirmation_email(
                request, new_form)
            return redirect("/")
        else:
            return render(request, "accounts/signup.html", {"form": form})

    if request.method == "GET":
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def Login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return HttpResponse("User does not exist")
            if user.is_verified:
                # authenticate the user
                user = authenticate(request, email=email, password=password)
                if user is None:
                    messages.warning(request, "Wrong credntials provided")
                    return redirect("account:login")
                else:
                    login(request, user)
                    messages.success(request, "Login successfully done")
                    next_url = request.GET.get("next", '/')
                    return redirect(next_url)
            else:
                messages.warning(request, "Email not verified.")
                context = {
                    "form": form
                }
                return render(request, "accounts/login.html", context)
    return render(request, "accounts/login.html", {"form": form})


def Logout(request):
    logout(request)
    messages.success(request, "Logout Done Successfully")
    return redirect("/")
