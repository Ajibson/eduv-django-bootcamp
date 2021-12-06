from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class User(AbstractUser):
    status_choice = (
        ("job_seeker", "Job Seeker"), ("recuiter", "recuiter")
    )
    gender_choice = (
        ("Male", "Male"), ("Female", "Female")
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    status = models.CharField(max_length=15, choices=status_choice)
    is_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=gender_choice, null=True)
    username = models.CharField(max_length=250, blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["password", "username"]

    def get_absolute_url(self):
        return f"/account/{self.id}"


class job_seeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to="job_seeker_image", blank=True)
    resume = models.FileField(upload_to="resume_file", validators=[
                              FileExtensionValidator(allowed_extensions=['pdf'])], blank=True)
    current_location = models.CharField(max_length=300, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    website = models.URLField(blank=True)
    company_name = models.CharField(max_length=250, blank=True)
    company_logo = models.ImageField(upload_to="company_logo", blank=True)
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)


@receiver(post_save, sender=User)
def create_job_seeker_recruiter(sender, instance, created, **kwargs):
    if created:
        if instance.status == "job_seeker":
            job_seeker.objects.create(user=instance)
        elif instance.status == "recuiter":
            recruiter.objects.create(user=instance)


class confirmation_email(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token
