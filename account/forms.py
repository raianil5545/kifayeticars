from django import forms

from .models import AppUser


class RegisterForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ("first_name", "last_name", "email", "password")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class LogInForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ("email", "password")
        widgets = {
                'email': forms.TextInput(attrs={'class': 'form-control'}),
                'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
