from django.shortcuts import render


def blogs(request):
    return render(request, 'blogs/blog.html')


def single_blog(request):

    return render(request, 'blogs/single-blog.html')
