from django import forms
from .models import Post, Comment
from subreddits.models import Subreddit

class PostCreateForm(forms.ModelForm):
    subreddit = forms.ModelChoiceField(
        queryset=Subreddit.objects.filter(approval_status='approved'),
        widget=forms.Select(attrs={
            'class': 'select2 w-full px-3 py-2 border rounded-md',
            'data-placeholder': 'Search for a subreddit...'
        }),
        required=True,
        error_messages={
            'required': 'Please select a subreddit',
            'invalid_choice': 'Please select a valid subreddit'
        }
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'url', 'image', 'subreddit']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'placeholder': 'Enter your post title'
            }),
            'content': forms.Textarea(attrs={
                'rows': 6,
                'class': 'w-full px-3 py-2 border rounded-md',
                'placeholder': 'Write your post content here...'
            }),
            'post_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-md'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'placeholder': 'Enter URL'
            }),
            'image': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'hidden'
            }),
        }
        error_messages = {
            'title': {
                'required': 'Please enter a title for your post',
                'max_length': 'Title must be less than 300 characters'
            },
            'content': {
                'required': 'Please enter content for your post'
            },
            'url': {
                'required': 'Please enter a URL for link posts',
                'invalid': 'Please enter a valid URL'
            },
            'image': {
                'required': 'Please select an image for image posts',
                'invalid': 'Please upload a valid image file'
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get('post_type')
        content = cleaned_data.get('content')
        url = cleaned_data.get('url')
        image = cleaned_data.get('image')

        if post_type == 'text' and not content:
            self.add_error('content', 'Content is required for text posts')
        elif post_type == 'link':
            if not url:
                self.add_error('url', 'URL is required for link posts')
            elif not url.startswith(('http://', 'https://')):
                self.add_error('url', 'Please enter a valid URL starting with http:// or https://')
        elif post_type == 'image':
            if not image and not self.instance.image:
                self.add_error('image', 'Image is required for image posts')
            elif image:
                # Validate image file
                if not image.content_type.startswith('image/'):
                    self.add_error('image', 'Please upload a valid image file')
                elif image.size > 5 * 1024 * 1024:  # 5MB limit
                    self.add_error('image', 'Image size should not exceed 5MB')
                else:
                    # Validate file extension
                    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
                    if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
                        self.add_error('image', 'Please upload a valid image file (JPG, JPEG, PNG, or GIF)')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Clear unnecessary fields based on post type
        if instance.post_type == 'text':
            instance.url = None
            instance.image = None
        elif instance.post_type == 'link':
            instance.content = ''
            instance.image = None
        elif instance.post_type == 'image':
            instance.content = ''
            instance.url = None
        
        if commit:
            try:
                # Save the instance first
                instance.save()
                
                # Handle image upload separately
                if 'image' in self.cleaned_data and self.cleaned_data['image']:
                    instance.image = self.cleaned_data['image']
                    instance.save(update_fields=['image'])
                
                # Handle URL for link posts
                if instance.post_type == 'link' and 'url' in self.cleaned_data:
                    instance.url = self.cleaned_data['url']
                    instance.save(update_fields=['url'])
                
                # Handle content for text posts
                if instance.post_type == 'text' and 'content' in self.cleaned_data:
                    instance.content = self.cleaned_data['content']
                    instance.save(update_fields=['content'])
                
            except Exception as e:
                raise forms.ValidationError(f"Error saving post: {str(e)}")
        
        return instance

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-3 py-2 border rounded-md',
                'placeholder': 'Write a comment...'
            })
        } 