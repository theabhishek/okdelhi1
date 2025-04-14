from django import forms
from .models import Subreddit

class SubredditCreateForm(forms.ModelForm):
    class Meta:
        model = Subreddit
        fields = ['name', 'description', 'rules', 'banner', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-3 py-2 border rounded-md'}),
            'rules': forms.Textarea(attrs={'rows': 6, 'class': 'w-full px-3 py-2 border rounded-md'}),
            'banner': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'icon': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
        }

class SubredditUpdateForm(forms.ModelForm):
    class Meta:
        model = Subreddit
        fields = ['description', 'rules', 'banner', 'icon']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-3 py-2 border rounded-md'}),
            'rules': forms.Textarea(attrs={'rows': 6, 'class': 'w-full px-3 py-2 border rounded-md'}),
            'banner': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'icon': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
        } 