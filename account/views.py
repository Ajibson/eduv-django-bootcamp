from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def signup(request):
    return render(request, 'account/signup.html')


def Login(request):
    return render(request, 'account/login.html')
