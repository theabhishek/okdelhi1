from django import forms
from .models import News, NewsComment

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'featured_image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter news title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 10,
                'placeholder': 'Write your news content here...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter tags separated by commas'
            }),
            'featured_image': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg file:bg-blue-600 file:text-white file:rounded file:px-4 file:py-1'
            }),
        }

class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }
