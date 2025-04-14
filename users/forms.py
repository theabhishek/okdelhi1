from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove specific password validation messages
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        # Remove specific validation messages
        for field in self.fields.values():
            field.error_messages = {
                'required': 'This field is required.',
                'invalid': 'Please enter a valid value.',
            }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avatar', 'bio')
        widgets = {
            'username': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES}),
            'avatar': forms.FileInput(attrs={'class': INPUT_CLASSES}),
            'bio': forms.Textarea(attrs={'class': f'{INPUT_CLASSES} h-24'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'avatar')
        widgets = {
            'username': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES}),
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'bio': forms.Textarea(attrs={'class': INPUT_CLASSES}),
            'avatar': forms.FileInput(attrs={'class': INPUT_CLASSES}),
        }
