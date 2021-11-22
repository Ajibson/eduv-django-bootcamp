# Generated by Django 3.2.9 on 2021-11-12 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_job_seeker'),
    ]

    operations = [
        migrations.CreateModel(
            name='recruiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField(blank=True)),
                ('company_name', models.CharField(max_length=250)),
                ('company_logo', models.ImageField(upload_to='company_logo')),
                ('address', models.CharField(max_length=300)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
