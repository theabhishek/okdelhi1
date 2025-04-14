from django.db import models
from django.utils.text import slugify
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

class Area(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='delhi_wiki/areas/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='verified_areas')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_areas')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # If the slug already exists, add a number suffix
            original_slug = self.slug
            counter = 1
            while Area.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class Landmark(models.Model):
    CATEGORIES = (
        ('historical', 'Historical'),
        ('religious', 'Religious'),
        ('modern', 'Modern'),
        ('cultural', 'Cultural'),
    )
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='landmarks')
    image = models.ImageField(upload_to='delhi_wiki/landmarks/', null=True, blank=True)
    address = models.TextField()
    timings = models.CharField(max_length=200)
    entry_fee = models.CharField(max_length=100, blank=True)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='verified_landmarks')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_landmarks')

    def __str__(self):
        return f"{self.name} - {self.area.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # If the slug already exists, add a number suffix
            original_slug = self.slug
            counter = 1
            while Landmark.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class FoodPlace(models.Model):
    CUISINES = (
        ('indian', 'Indian'),
        ('chinese', 'Chinese'),
        ('italian', 'Italian'),
        ('mexican', 'Mexican'),
        ('fast_food', 'Fast Food'),
        ('street_food', 'Street Food'),
        ('desserts', 'Desserts'),
    )
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    cuisine = models.CharField(max_length=20, choices=CUISINES)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='food_places')
    image = models.ImageField(upload_to='delhi_wiki/food_places/', null=True, blank=True)
    address = models.TextField()
    timings = models.CharField(max_length=200)
    price_range = models.CharField(max_length=100)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='verified_food_places')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_food_places')

    def __str__(self):
        return f"{self.name} - {self.area.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # If the slug already exists, add a number suffix
            original_slug = self.slug
            counter = 1
            while FoodPlace.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class Market(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='markets')
    image = models.ImageField(upload_to='delhi_wiki/markets/', null=True, blank=True)
    address = models.TextField()
    timings = models.CharField(max_length=200)
    specialties = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='verified_markets')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_markets')

    def __str__(self):
        return f"{self.name} - {self.area.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # If the slug already exists, add a number suffix
            original_slug = self.slug
            counter = 1
            while Market.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class Event(models.Model):
    CATEGORIES = (
        ('concert', 'Concert'),
        ('exhibition', 'Exhibition'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('food', 'Food'),
        ('shopping', 'Shopping'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    venue = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='events')
    image = models.ImageField(upload_to='delhi_wiki/events/', null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    ticket_price = models.CharField(max_length=100, blank=True)
    ticket_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='verified_events')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_events')

    def __str__(self):
        return f"{self.title} - {self.area.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # If the slug already exists, add a number suffix
            original_slug = self.slug
            counter = 1
            while Event.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class LandmarkReview(Review):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='landmark_reviews')

class FoodPlaceReview(Review):
    food_place = models.ForeignKey(FoodPlace, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='food_place_reviews')

class MarketReview(Review):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='market_reviews')

class EventReview(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='event_reviews')
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}'s review of {self.event.title}"

    class Meta:
        ordering = ['-created_at']

class MetroLine(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class MetroStation(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    lines = models.ManyToManyField('MetroLine', related_name='stations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_interchange = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='delhi_wiki/metro_stations/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            # Check if slug exists (excluding current instance if updating)
            while MetroStation.objects.filter(
                Q(slug=slug) & ~Q(pk=self.pk) if self.pk else Q(slug=slug)
            ).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

class MetroRoute(models.Model):
    source = models.ForeignKey(MetroStation, on_delete=models.CASCADE, related_name='routes_from')
    destination = models.ForeignKey(MetroStation, on_delete=models.CASCADE, related_name='routes_to')
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    fare = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.IntegerField(help_text='Estimated journey time in minutes')
    interchange_stations = models.ManyToManyField(MetroStation, related_name='route_interchanges', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source.name} to {self.destination.name}"

    class Meta:
        unique_together = ('source', 'destination')
