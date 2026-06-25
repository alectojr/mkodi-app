from django import forms
from .models import Taxpayer


class TaxpayerForm(forms.ModelForm):
    class Meta:
        model = Taxpayer
        fields = ['tin_number', 'full_name', 'phone_number', 'email', 'business_name', 'brela_number']
        widgets = {
            'tin_number': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brela_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
