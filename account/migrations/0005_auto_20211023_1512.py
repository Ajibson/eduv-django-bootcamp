# Generated by Django 3.2.8 on 2021-10-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_account_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_seeker',
            name='availability',
            field=models.CharField(blank=True, choices=[('Available for employment', 'Available for employment'), ('Not available for employment', 'Not available for employment')], max_length=100),
        ),
        migrations.AddField(
            model_name='job_seeker',
            name='current_location',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='job_seeker',
            name='min_salary',
            field=models.PositiveIntegerField(blank=True, default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job_seeker',
            name='title',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='job_seeker',
            name='skills',
            field=models.TextField(blank=True, help_text='comma separated skills'),
        ),
    ]
