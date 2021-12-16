from django import forms
from .models import jobs, Category


class JobForm(forms.ModelForm):
    class Meta:
        model = jobs
        exclude = ["posted_by", "date_posted"]
