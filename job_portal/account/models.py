from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    status_choice = (
        ("job_seeker", "Job Seeker"), ("recuiter", "recuiter")
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=70)
    status = models.CharField(max_length=15, choices=status_choice)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["password", "username"]


class job_seeker(models.Model):
    phone_number = models.CharField(max_length=20)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="job_seeker_image")
    resume = models.FileField(upload_to="resume_file")
    current_location = models.CharField(max_length=300)
    bio = models.TextField()
