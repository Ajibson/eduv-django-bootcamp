from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import User, job_seeker, recruiter


# admin.site.register(User)
admin.site.register(job_seeker)

# admin.site.register(recruiter)


@admin.register(recruiter)
class recruiterAdmin(ImportExportModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', "is_verified", "get_full_name")
    list_filter = ["is_verified"]
    search_fields = ["email"]
    fields = ["email", "password", "is_verified",
              "first_name", "last_name", "status"]


# admin.site.register(recruiter, recruiterAdmin)
