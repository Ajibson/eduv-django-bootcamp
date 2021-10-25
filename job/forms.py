from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ['date_created']

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['Knowledge_skills_abilities'].widget.attrs.update(
            {'rows': 4})
        self.fields['job_description'].widget.attrs.update(
            {'rows': 4})
        self.fields['education_experience'].widget.attrs.update(
            {'rows': 4})
        self.fields['application_deadline'].widget.attrs.update(
            {'placeholder': "yyyy-mm-dd"})
