from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import AppUser


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="Enter First name", max_length=50, help_text="*")
    last_name = forms.CharField(label="Enter last name", max_length=50)
    email = forms.EmailField(label="Enter Email", help_text="*",
                             error_messages={'required': "Enter a valid email"})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ("first_name", "last_name", "email", "password")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if AppUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email

    def clean_password2(self):
        clean_data = self.cleaned_data
        if clean_data['password'] != clean_data['password2']:
            raise forms.ValidationError("Password doesn't match")
        return clean_data["password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'last name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'User Email', 'id': 'login-email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))
