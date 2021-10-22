from django.contrib import admin

from .models import Account, job_seeker, recuiter

admin.site.register(Account)
admin.site.register(job_seeker)
admin.site.register(recuiter)
