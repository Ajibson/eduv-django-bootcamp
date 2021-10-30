from django.contrib import admin
from .models import Job, Category


class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'category',
                    'job_nature', 'date_created', "salary_range", "confirmed"]
    list_filter = ['category', 'job_nature']


admin.site.register(Job, JobAdmin)
admin.site.register(Category)
