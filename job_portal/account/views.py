from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from .forms import SignUpForm, LoginForm


def signup(request):

    if request.method == "POST":
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # email = request.POST['email']
        # password = request.POST['password']
        # status = request.POST['status']
        # user = User.objects.create(
        #     first_name=first_name, last_name=last_name, email=email, password=password, status=status)
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.set_password(form.cleaned_data['password'])
            new_form.save()
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
                return redirect("/")
            else:
                msg = "Please verify your email"
                context = {
                    "form": form, "msg": msg
                }
                return render(request, "accounts/login.html", context)
    return render(request, "accounts/login.html", {"form": form})
