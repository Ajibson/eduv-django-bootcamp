from django.contrib import admin

from .models import Account, job_seeker, recuiter


class AccountAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Primary Information", {
            'fields': (('first_name', 'last_name'), ('email', 'username'), ('password', 'last_login'), ('is_active', 'status'))
        }),
        ("Permissions", {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions')
        }),
        ('Related information', {
            'classes': ('collapse',),
            'fields': ('phone_number', "is_verified"),
        }),
    )
    list_display = ['email', 'first_name']


admin.site.register(Account, AccountAdmin)
admin.site.register(job_seeker)
admin.site.register(recuiter)
