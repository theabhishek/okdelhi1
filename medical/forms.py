from django import forms
from .models import MedicalFacility

class MedicalFacilityForm(forms.ModelForm):
    class Meta:
        model = MedicalFacility
        fields = [
            'name', 'facility_type', 'address', 'location', 'city',
            'contact_number', 'email', 'website', 'description',
            'services', 'opening_hours'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'placeholder': 'Enter facility name'}),
            'facility_type': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'contact_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'website': forms.URLInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={
                'rows': 3, 'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Brief description of the facility'
            }),
            'services': forms.Textarea(attrs={
                'rows': 3, 'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'List of services provided'
            }),
            'opening_hours': forms.Textarea(attrs={
                'rows': 2, 'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'e.g., Mon-Fri: 9am-5pm'
            }),
        }
