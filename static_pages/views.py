from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import cloudinary.uploader

# Create your views here.

class HomeView(TemplateView):
    template_name = 'static_pages/home.html'

class AboutView(TemplateView):
    template_name = 'static_pages/about.html'

class TermsView(TemplateView):
    template_name = 'static_pages/terms.html'

class PrivacyView(TemplateView):
    template_name = 'static_pages/privacy.html'

def test_cloudinary(request):
    try:
        # Upload a test image
        result = cloudinary.uploader.upload(
            "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg",
            folder="test_uploads"
        )
        
        # Return the upload result
        return HttpResponse(f"Cloudinary test successful! Image URL: {result['secure_url']}")
    except Exception as e:
        return HttpResponse(f"Cloudinary test failed: {str(e)}")
