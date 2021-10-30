from django.contrib import admin

from .models import blogs, Category, Author


@admin.register(blogs)
class blogAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']


@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Author)
