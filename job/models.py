from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    flaticon = models.CharField(max_length=250, blank=True)

    def __str__(self) -> str:
        return self.name


class CategoryOption(models.TextChoices):

    for i in Category.objects.all():
        print(i)
        f"{i.name}", f"{i.name}"


class Job(models.Model):
    job_nature_choices = (
        ("Part Time", "Part Time"), ("Full Time", "Full Time")
    )
    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=255, choices=CategoryOption.choices)
    job_nature = models.CharField(max_length=25, choices=job_nature_choices)
    application_link = models.URLField(default="https://", blank=True)
    application_email = models.EmailField(blank=True)
    salary_range = models.CharField(
        max_length=200, help_text="e.g $500 - $900")
    application_deadline = models.DateField(blank=True)
    slot_available = models.PositiveIntegerField(default=1)
    Knowledge_skills_abilities = models.TextField(
        blank=True, help_text="End each input with comma e.g System Software Development,Strong problem solving and debugging skills")
    education_experience = models.TextField(
        blank=True, help_text='End each input with comma e.g 3 or more years of professional design experience,Direct response email experience')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
