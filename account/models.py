from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

from .email import send_confirnation_email

from django.utils import timezone


class Account(AbstractUser):
    status_choices = (
        ('job_seeker', 'job_seeker'), ('recuiter', 'recuiter')
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200, blank=True)
    status = models.CharField(
        max_length=20, choices=status_choices, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']

    def __str__(self):
        return self.email


class job_seeker(models.Model):
    gender_choice = (
        ('Male', 'Male'), ('Female', 'Female')
    )
    availablity_choice = (
        ("Available for employment", "Available for employment"), (
            "Not available for employment", "Not available for employment")
    )
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="job_seeker_account", blank=True, null=True)
    title = models.CharField(max_length=500, blank=True)
    min_salary = models.PositiveIntegerField(default=0)
    current_location = models.CharField(max_length=500, blank=True)
    resume = models.FileField(blank=True, upload_to="job_seeker_resume", validators=[
                              FileExtensionValidator(allowed_extensions=['pdf'])])
    image = models.ImageField(blank=True, upload_to="profile_image")
    skills = models.TextField(blank=True, help_text="comma separated skills")
    gender = models.CharField(max_length=20, blank=True, choices=gender_choice)
    availability = models.CharField(
        max_length=100, blank=True, choices=availablity_choice)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.title}"


class recuiter(models.Model):
    employment_choice = (
        ("Hiring", "Hiring"), ("Firing", "Firing"), ("Freeze Mode",
                                                     "Freeze Mode"), ("Laying Off", "Laying Off")
    )
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="recuiter_account")
    company_name = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    current_location = models.CharField(max_length=300, blank=True)
    employment_state = models.CharField(
        max_length=100, blank=True, choices=employment_choice)
    website = models.URLField(blank=True, default="https://")
    email = models.EmailField(blank=True)
    logo = models.ImageField(blank=True, upload_to="recuiter_company_logo")
    cleared = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.company_name


@receiver(post_save, sender=Account)
def create_job_seeker_recuiter(sender, instance, created, **kwargs):
    if created and instance.status == "job_seeker":
        new_job_seeker = job_seeker.objects.create(user=instance)
        # Send confirmation email with the link to update the profile
        send_email = send_confirnation_email(instance)
    elif created and instance.status == 'recuiter':
        new_recuiter = recuiter.objects.create(user=instance)
        # Send confirmation email with the link to update the profile
        send_email = send_confirnation_email(instance)


class passwordresetcode(models.Model):
    code = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
