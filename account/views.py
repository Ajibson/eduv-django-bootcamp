from django.shortcuts import render, redirect

from account.models import Account
from .forms import SignUpForm

from django.contrib import messages
from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


def index(request):
    return render(request, "index.html")


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
            messages.success(request, "Registration Successfully")
            return redirect("index")
        else:
            return render(request, 'account/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def Login(request):
    return render(request, 'account/login.html')


def password_reset(request):
    return render(request, 'account/password_reset.html')


def account_confirmation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None:
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        # invalid link
        messages.error(request, "Invalid Link")
        return render(request, 'account/signup.html')
