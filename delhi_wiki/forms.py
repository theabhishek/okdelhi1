from django import forms
from .models import Area, Landmark, FoodPlace, Market, Event, LandmarkReview, FoodPlaceReview, MarketReview, EventReview

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name', 'description', 'location', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'location': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'image': forms.FileInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
        }

class LandmarkForm(forms.ModelForm):
    class Meta:
        model = Landmark
        fields = ['name', 'description', 'category', 'area', 'image', 'address', 'timings', 'entry_fee', 'rating']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'timings': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'entry_fee': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'image': forms.FileInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'category': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'area': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'rating': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500', 'min': '0', 'max': '5', 'step': '0.1'}),
        }

class FoodPlaceForm(forms.ModelForm):
    class Meta:
        model = FoodPlace
        fields = ['name', 'description', 'cuisine', 'area', 'image', 'address', 'timings', 'price_range', 'rating']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'timings': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'price_range': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'image': forms.FileInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'cuisine': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'area': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'rating': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500', 'min': '0', 'max': '5', 'step': '0.1'}),
        }

class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ['name', 'description', 'area', 'image', 'address', 'timings', 'specialties']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'timings': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'specialties': forms.Textarea(attrs={'rows': 2, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'image': forms.FileInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'area': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'venue', 'area', 'image', 'start_date', 'end_date', 'ticket_price', 'ticket_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'title': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'venue': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'ticket_price': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'ticket_link': forms.URLInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'image': forms.FileInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'category': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'area': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'rating': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
        }

class LandmarkReviewForm(ReviewForm):
    class Meta(ReviewForm.Meta):
        model = LandmarkReview

class FoodPlaceReviewForm(ReviewForm):
    class Meta(ReviewForm.Meta):
        model = FoodPlaceReview

class MarketReviewForm(ReviewForm):
    class Meta(ReviewForm.Meta):
        model = MarketReview

class EventReviewForm(forms.ModelForm):
    class Meta:
        model = EventReview
        fields = ['rating', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'}),
            'rating': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500', 'min': '0', 'max': '5', 'step': '0.1'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Search areas, landmarks, food places...'
        })
    ) 