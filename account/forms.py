from django import forms
from .models import Account


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
        if not password.isalnum:
            raise forms.ValidationError(
                "Password should contain both numbers and letters")

        return password


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
