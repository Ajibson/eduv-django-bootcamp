from django.shortcuts import render
from .models import blogs, Category
from taggit.models import Tag
from django.views import View
from django.core.paginator import Paginator
from .next_prev import prev_next


def common():
    gotten_blogs = blogs.objects.filter(
        status="Published").order_by("-date_published")
    categories = Category.objects.all()
    tags = Tag.objects.all()
    cat_dict = {}
    for category in categories:
        blog_categories = blogs.objects.filter(category=category.pk)
        cat_dict[category] = len(blog_categories)
    return gotten_blogs, categories, cat_dict, tags


class blogs_posts(View):

    def get(self, request):
        gotten_blogs, categories, cat_dict, tags = common()
        paginator = Paginator(gotten_blogs, 1)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj, 'cat_dict': cat_dict, 'blogs': gotten_blogs, "recent_blogs": gotten_blogs[:4], "tags": tags, "categories": categories
        }
        return render(request, 'blogs/blog.html', context)


def single_blog(request, blog_slug):
    blog_gotten = blogs.objects.filter(slug=blog_slug).first()
    gotten_blogs, categories, cat_dict, tags = common()
    prev_blog, next_blog = prev_next(blog_gotten)
    context = {
        "blog": blog_gotten, 'cat_dict': cat_dict, "recent_blogs": gotten_blogs[:4], "categories": categories, "tags": tags,
        "prev_blog": prev_blog, "next_blog": next_blog
    }
    return render(request, 'blogs/single-blog.html', context)
