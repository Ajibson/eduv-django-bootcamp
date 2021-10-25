from django import forms
from .models import Account, job_seeker, recuiter
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):

    confirm_password = forms.CharField(
        min_length=8, widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'password', 'confirm_password', 'status']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already used, Please login instead")

        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("phone_number already used.")

        return phone_number

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if confirm_password != password:
            raise forms.ValidationError("Passwords do not match")
        if len(password) < 8:
            raise forms.ValidationError(
                "Password should be min of 8 characters")
        if password.isalpha() or password.isnumeric():
            raise forms.ValidationError(
                "Password should contain both numbers and letters")

        return password


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class job_seekerForm(forms.ModelForm):

    class Meta:
        model = job_seeker
        fields = ['title', 'image', 'gender',
                  'resume', 'min_salary', "current_location", 'skills', 'bio', "availability"]

    def __init__(self, *args, **kwargs):
        super(job_seekerForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['skills'].widget.attrs.update(
            {'placeholder': 'Comma separated skill', 'rows': 3})
        self.fields['current_location'].widget.attrs.update(
            {'placeholder': 'State and Country only'})
        self.fields['bio'].widget.attrs.update(
            {'placeholder': 'Summary your yourself', 'rows': 3})
        self.fields['title'].widget.attrs.update(
            {'placeholder': 'e.g Software Developer'})


class CompanyForm(forms.ModelForm):

    class Meta:
        model = recuiter
        fields = ['company_name', 'website',
                  'current_location', 'logo', "email", 'employment_state', "description"]

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['description'].widget.attrs.update(
            {'placeholder': 'Describe the company', 'rows': 3})
        self.fields['current_location'].widget.attrs.update(
            {'placeholder': 'State and Country only e.g Jigawa,Nigeria'})


class NewPasswordResetForm(forms.Form):
    # password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")

        # check password length
        if len(confirm_password) < 8:
            raise ValidationError("Password can't be less than 8 characters")
        # check for number and letters is password
        if confirm_password.isalpha() or confirm_password.isnumeric():
            raise ValidationError(
                "Password should contains both letters and numbers")

        return confirm_password
