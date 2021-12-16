from django.db import models
from account.models import recruiter
from django.utils import timezone


class jobs(models.Model):
    posted_by = models.ForeignKey(recruiter, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250)
    location = models.CharField(max_length=300)
    application_email = models.EmailField()
    appliction_url = models.URLField(blank=True)
    application_deadline = models.DateField(blank=True, null=True)
    salary = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    education_experience = models.TextField()
    requirements = models.TextField()
    slots = models.IntegerField()
    job_nature = models.CharField(
        max_length=200, choices=(("Full Time", "Full Time"), ("Part Time", "Part Time"))
    )
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Jobs"


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
