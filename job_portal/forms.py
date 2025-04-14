from django import forms
from .models import Job, JobApplication, JobCategory # Assuming these models exist

# Define a base style to reuse
tailwind_input_classes = (
    "shadow appearance-none border border-gray-300 rounded w-full py-2 px-3 "
    "text-gray-700 leading-tight focus:outline-none focus:ring-2 "
    "focus:ring-indigo-200 focus:border-indigo-500"
)

tailwind_textarea_classes = f"{tailwind_input_classes} h-auto" # Allow textareas to resize vertically based on rows
tailwind_select_classes = tailwind_input_classes # Base style works for select too, appearance-none helps remove default dropdown arrow styling

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company', 'location', 'description', 'requirements',
            'salary_min', 'salary_max', 'category', 'job_type', 'experience_min',
            'experience_max', 'education', 'skills', 'benefits', 'application_deadline',
            'contact_email', 'contact_phone', 'website'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Job Title'}),
            'company': forms.TextInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Company Name'}),
            'location': forms.TextInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Job Location'}),
            'description': forms.Textarea(attrs={'class': tailwind_textarea_classes, 'rows': 4, 'placeholder': 'Job Description'}),
            'requirements': forms.Textarea(attrs={'class': tailwind_textarea_classes, 'rows': 4, 'placeholder': 'Job Requirements'}),
            'salary_min': forms.NumberInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Minimum Salary'}),
            'salary_max': forms.NumberInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Maximum Salary'}),
            # Assuming category is a ForeignKey to JobCategory
            'category': forms.Select(attrs={'class': tailwind_select_classes}),
            # Assuming job_type uses choices
            'job_type': forms.Select(attrs={'class': tailwind_select_classes}),
            'experience_min': forms.NumberInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Minimum Experience (years)'}),
            'experience_max': forms.NumberInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Maximum Experience (years)'}),
            'education': forms.TextInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Required Education'}),
            'skills': forms.Textarea(attrs={'class': tailwind_textarea_classes, 'rows': 3, 'placeholder': 'Required Skills (comma-separated)'}),
            'benefits': forms.Textarea(attrs={'class': tailwind_textarea_classes, 'rows': 3, 'placeholder': 'Job Benefits'}),
            # Note: Date input styling can be browser-dependent
            'application_deadline': forms.DateInput(attrs={'class': tailwind_input_classes, 'type': 'date'}),
            'contact_email': forms.EmailInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Contact Email'}),
            'contact_phone': forms.TextInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Contact Phone'}),
            'website': forms.URLInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Company Website (https://...)'}),
        }

    # Optional: Add __init__ if you need to set queryset for ForeignKey fields like category
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['category'].queryset = JobCategory.objects.all()
    #     # Add empty label option if desired
    #     self.fields['category'].empty_label = "Select Category"
    #     # Similarly for job_type if it's a ForeignKey, otherwise choices are set in the model

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume_link']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': tailwind_textarea_classes, 'rows': 5, 'placeholder': 'Write your cover letter here...'}),
            'resume_link': forms.URLInput(attrs={'class': tailwind_input_classes, 'placeholder': 'Link to your Resume (e.g., Google Drive, Dropbox, LinkedIn)'}),
            # Consider using forms.FileField for actual uploads instead of just a link
            # 'resume_file': forms.ClearableFileInput(attrs={'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'})
        }