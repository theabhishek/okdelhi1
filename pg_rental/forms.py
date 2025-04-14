from django import forms
from .models import PGListing, Booking, Review

class PGListingForm(forms.ModelForm):
    image1 = forms.ImageField(required=True, label='Primary Image', widget=forms.ClearableFileInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}))
    image2 = forms.ImageField(required=False, label='Additional Image 1', widget=forms.ClearableFileInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}))
    image3 = forms.ImageField(required=False, label='Additional Image 2', widget=forms.ClearableFileInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}))
    image4 = forms.ImageField(required=False, label='Additional Image 3', widget=forms.ClearableFileInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}))
    image5 = forms.ImageField(required=False, label='Additional Image 4', widget=forms.ClearableFileInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}))

    class Meta:
        model = PGListing
        fields = [
            'title', 'description', 'property_type', 'gender_preference',
            'price_per_month', 'locality', 'city', 'state', 'pincode'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md', 'rows': 4}),
            'property_type': forms.Select(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}),
            'gender_preference': forms.Select(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}),
            'price_per_month': forms.NumberInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}),
            'locality': forms.TextInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}),
            'city': forms.TextInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}),
            'state': forms.TextInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}),
            'pincode': forms.TextInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md', 'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md'}),
            'comment': forms.Textarea(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-md', 'rows': 4}),
        }
