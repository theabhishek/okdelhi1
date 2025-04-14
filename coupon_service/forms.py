from django import forms
from .models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            'title', 'description', 'store', 'affiliate_link',
            'discount_percentage', 'discount_amount', 'valid_from',
            'valid_until', 'is_active', 'image', 'terms_and_conditions'
        ]
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'terms_and_conditions': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_class = 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        checkbox_class = 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': checkbox_class})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': tailwind_class + ' file:bg-blue-500 file:text-white file:px-4 file:py-1'})
            else:
                field.widget.attrs.update({'class': tailwind_class})

    def clean(self):
        cleaned_data = super().clean()
        discount_percentage = cleaned_data.get('discount_percentage')
        discount_amount = cleaned_data.get('discount_amount')

        if discount_percentage and discount_amount:
            raise forms.ValidationError("Please provide either discount percentage or amount, not both.")

        if not discount_percentage and not discount_amount:
            raise forms.ValidationError("Please provide either discount percentage or amount.")

        return cleaned_data
