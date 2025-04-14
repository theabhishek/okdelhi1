from django import forms
from .models import Notification, NotificationComment

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'priority', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class NotificationCommentForm(forms.ModelForm):
    class Meta:
        model = NotificationComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class NotificationApprovalForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        } 