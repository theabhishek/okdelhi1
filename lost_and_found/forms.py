from django import forms
from .models import LostAndFoundItem

class LostAndFoundItemForm(forms.ModelForm):
    class Meta:
        model = LostAndFoundItem
        fields = ['item_type', 'title', 'description', 'location', 'date_lost_found', 'contact_number', 'image']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'rows': 4
            }),
            'location': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'date_lost_found': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 border border-gray-300 rounded'
            }),
            'contact_number': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
        }
