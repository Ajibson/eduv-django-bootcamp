from django.db import models
from account.models import recuiter
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    flaticon = models.CharField(max_length=250, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class CategoryOption(models.TextChoices):
    Web_Developement = "Web Development", "Web Development"
    Graphic_Design = "Graphic Design", "Graphic Design"
    Others = "Others", "Others"


class JobNatureOption(models.TextChoices):
    Full_Time = "Full Time", "Full Time"
    Part_Time = "Part Time", "Part Time"


class Job(models.Model):
    job_nature_choices = (
        ("Part Time", "Part Time"), ("Full Time", "Full Time")
    )
    posted_by = models.ForeignKey(
        recuiter, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=255, choices=CategoryOption.choices, default=CategoryOption.Web_Developement)
    job_nature = models.CharField(
        max_length=25, choices=JobNatureOption.choices)
    application_link = models.URLField(default="https://", blank=True)
    application_email = models.EmailField(blank=True)
    salary_range = models.PositiveIntegerField()
    application_deadline = models.DateField(blank=True, help_text="yyyy-mm-dd")
    slot_available = models.PositiveIntegerField(default=1)
    job_description = models.TextField(blank=True)
    Knowledge_skills_abilities = models.TextField(
        blank=True, help_text="End each input with comma e.g System Software Development,Strong problem solving and debugging skills")
    education_experience = models.TextField(
        blank=True, help_text='End each input with comma e.g 3 or more years of professional design experience,Direct response email experience')
    date_created = models.DateTimeField(default=timezone.now)
    job_slug = models.SlugField(blank=True, null=True)
    confirmed = models.BooleanField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # the below action will be done every time any blog is being saved
        self.job_slug = slugify(self.title, allow_unicode=True)
        super(Job, self).save(*args, **kwargs)
