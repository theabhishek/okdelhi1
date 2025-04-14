from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content', 'category', 'location', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': 'Enter a catchy title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
                'rows': 10,
                'placeholder': 'Share your story...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': 'Where did this happen?'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),
        }
