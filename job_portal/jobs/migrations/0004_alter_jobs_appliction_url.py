# Generated by Django 3.2.9 on 2021-12-16 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_jobs_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='appliction_url',
            field=models.URLField(blank=True),
        ),
    ]
