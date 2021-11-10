from django.contrib import admin

from .models import User, job_seeker


admin.site.register(User)
admin.site.register(job_seeker)
