# File: buckets/forms.py
from django import forms
from .models import Bucket


class BucketForm(forms.ModelForm):
    class Meta:
        model = Bucket
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bucket name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional description'
            }),
        }
