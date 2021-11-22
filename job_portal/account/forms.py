from django import forms
from .models import User


class SignUpForm(forms.ModelForm):
    # choice_gender = (

    # )
    # first_name = forms.CharField(max_length=30, required=True)
    # last_name = forms.CharField(max_length=30, required=False)
    # email = forms.EmailField(max_length=254, required=True)
    # password = forms.CharField(widget=forms.PasswordInput, required=True)
    # phone_number = forms.CharField(max_length=13, required=True)
    #
    # gender = forms.CharField(max_length=10, required=True, choices=)

    confirm_password = forms.CharField(
        widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email",
                  "gender", "password", "status", "confirm_password"]  # "__all__"
        # excludes = ["first_name"]
        widgets = {
            "password": forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # self.fields['first_name'].widget.attrs.update({"cols": 3, "rows": 3})

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Password does not match")
        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long")
        if password.isdigit() or password.isalpha():
            raise forms.ValidationError(
                "Password must contain a letter and number")
        return password


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
