from django import forms
from .models import Stop, Route

class RouteSearchForm(forms.Form):
    origin = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type to search origin stop...',
            'id': 'origin-search',
            'list': 'origin-stops-list'
        })
    )
    origin_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    destination = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type to search destination stop...',
            'id': 'destination-search',
            'list': 'destination-stops-list'
        })
    )
    destination_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        origin_id = cleaned_data.get('origin_id')
        destination_id = cleaned_data.get('destination_id')

        if not origin_id:
            self.add_error('origin', "Please select a valid origin stop from the suggestions.")
        if not destination_id:
            self.add_error('destination', "Please select a valid destination stop from the suggestions.")

        if origin_id and destination_id:
            try:
                origin_stop = Stop.objects.get(stop_id=origin_id)
                destination_stop = Stop.objects.get(stop_id=destination_id)
                
                if origin_stop == destination_stop:
                    self.add_error('destination', "Origin and destination stops cannot be the same.")
                
                cleaned_data['origin'] = origin_stop
                cleaned_data['destination'] = destination_stop
            except Stop.DoesNotExist:
                if not cleaned_data.get('origin'):
                    self.add_error('origin', "Selected origin stop does not exist.")
                if not cleaned_data.get('destination'):
                    self.add_error('destination', "Selected destination stop does not exist.")

        return cleaned_data

class FareCalculationForm(forms.Form):
    route = forms.ModelChoiceField(
        queryset=Route.objects.all().order_by('route_short_name'),
        label='Select Route',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Route"
    )
    origin_stop = forms.ModelChoiceField(
        queryset=Stop.objects.all().order_by('stop_name'),
        label='Origin Stop',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Origin Stop"
    )
    destination_stop = forms.ModelChoiceField(
        queryset=Stop.objects.all().order_by('stop_name'),
        label='Destination Stop',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Destination Stop"
    )

    def clean(self):
        cleaned_data = super().clean()
        origin_stop = cleaned_data.get('origin_stop')
        destination_stop = cleaned_data.get('destination_stop')
        route = cleaned_data.get('route')

        if origin_stop and destination_stop and origin_stop == destination_stop:
            raise forms.ValidationError("Origin and destination stops cannot be the same.")

        if route and origin_stop and destination_stop:
            # Check if both stops are on the selected route
            if not route.trip_set.filter(stoptime__stop=origin_stop).exists():
                raise forms.ValidationError(f"Origin stop is not on the selected route.")
            if not route.trip_set.filter(stoptime__stop=destination_stop).exists():
                raise forms.ValidationError(f"Destination stop is not on the selected route.")

        return cleaned_data 