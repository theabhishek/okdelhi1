from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    karma = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return f"/u/{self.username}/"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users' 