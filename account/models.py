from django.db import models
from django.contrib.auth.models import AbstractUser

from django.dispatch import receiver
from django.db.models.signals import post_save


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    recuiter = models.BooleanField(default=False)
    job_seeker = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']

    def __str__(self):
        return self.email


class job_seeker(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="job_seeker_account")
    resume = models.FileField(blank=True, upload_to="job_seeker_resume")
    image = models.ImageField(blank=True, upload_to="profile_image")
    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.website}"


class recuiter(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="recuiter_account")
    name = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=300, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(blank=True, upload_to="recuiter_company_logo")

    def __str__(self) -> str:
        return super().__str__()


@receiver(post_save, sender=Account)
def create_job_seeker_recuiter(sender, instance, created, **kwargs):
    if created and instance.job_seeker:
        new_job_seeker = job_seeker.objects.create(user=instance)
        # Send confirmation email with the link to update the profile
    elif created and instance.recuiter:
        new_recuiter = recuiter.objects.create(user=instance)
        # Send confirmation email with the link to update the profile
