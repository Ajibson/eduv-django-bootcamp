# Generated by Django 3.2.8 on 2021-10-25 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0010_alter_job_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
