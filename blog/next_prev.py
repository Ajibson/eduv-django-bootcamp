from django.core.paginator import Paginator, EmptyPage
from .models import blogs


def prev_next(blog):
    bd_blogs = blogs.objects.order_by('-date_published', "title")
    # Break the pages into one course per page
    current_page = Paginator(bd_blogs, 1)
    # Loop through the all pages
    for page_number in range(1, current_page.num_pages+1):
        # Get each page
        page_obj = current_page.page(page_number)
        # Loop through the page i.e get the blog
        for entry in page_obj:
            # check if entry is equal to the course coming from front end
            if entry == blog:
                # Check if the current page has next page
                if page_obj.has_next:
                    # Get the page to get the course on the page
                    try:
                        next_page = current_page.page(
                            page_obj.next_page_number())
                        for obj in next_page:
                            next_obj = obj
                    except EmptyPage:
                        next_obj = "None"
                else:
                    next_obj = "None"
                if page_obj.has_previous:
                    # Get the page to get the course on the page
                    try:
                        prev_page = current_page.page(
                            page_obj.previous_page_number())
                        for obj in prev_page:
                            prev_obj = obj
                    except EmptyPage:
                        prev_obj = "None"
                else:
                    prev_obj = "None"
                return prev_obj, next_obj
            else:
                continue
