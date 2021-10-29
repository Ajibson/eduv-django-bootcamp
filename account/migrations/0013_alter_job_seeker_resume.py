# Generated by Django 3.2.8 on 2021-10-29 23:45

import cloudinary_storage.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_recuiter_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_seeker',
            name='resume',
            field=models.FileField(blank=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='job_seeker_resume', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]