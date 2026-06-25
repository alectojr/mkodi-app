from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):
    tin_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Tax ID Number'}
    ))
    full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name'}
    ))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone Number'}
    ))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email (optional)'}
    ))
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password (min 8 characters)'}
    ))
    password_confirm = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}
    ))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError('Passwords do not match.')

        tin_number = cleaned_data.get('tin_number')
        if User.objects.filter(username=tin_number).exists():
            raise ValidationError('This TIN is already registered.')

        return cleaned_data


class LoginForm(forms.Form):
    tin_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Tax ID Number'}
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))
