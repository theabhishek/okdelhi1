from django.db import models
from django.utils.text import slugify
from users.models import CustomUser
from subreddits.models import Subreddit

class Post(models.Model):
    POST_TYPES = (
        ('text', 'Text'),
        ('link', 'Link'),
        ('image', 'Image'),
    )
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField()
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(CustomUser, related_name='upvoted_posts', blank=True)
    downvotes = models.ManyToManyField(CustomUser, related_name='downvoted_posts', blank=True)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/r/{self.subreddit.slug}/post/{self.slug}/"
    
    def update_score(self):
        self.score = self.upvotes.count() - self.downvotes.count()
        self.save()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(CustomUser, related_name='upvoted_comments', blank=True)
    downvotes = models.ManyToManyField(CustomUser, related_name='downvoted_comments', blank=True)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    def update_score(self):
        self.score = self.upvotes.count() - self.downvotes.count()
        self.save()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments' 