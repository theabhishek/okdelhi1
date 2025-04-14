from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Agency(models.Model):
    agency_id = models.CharField(max_length=100, unique=True)
    agency_name = models.CharField(max_length=200)
    agency_url = models.URLField()
    agency_timezone = models.CharField(max_length=100)
    agency_lang = models.CharField(max_length=10, null=True, blank=True)
    agency_phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.agency_name

class Route(models.Model):
    ROUTE_TYPES = (
        (0, 'Tram, Streetcar, Light rail'),
        (1, 'Subway, Metro'),
        (2, 'Rail'),
        (3, 'Bus'),
        (4, 'Ferry'),
        (5, 'Cable tram'),
        (6, 'Aerial lift'),
        (7, 'Funicular'),
        (11, 'Trolleybus'),
        (12, 'Monorail'),
    )

    route_id = models.CharField(max_length=100, unique=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    route_short_name = models.CharField(max_length=50)
    route_long_name = models.CharField(max_length=200)
    route_desc = models.TextField(null=True, blank=True)
    route_type = models.IntegerField(choices=ROUTE_TYPES)
    route_url = models.URLField(null=True, blank=True)
    route_color = models.CharField(max_length=6, null=True, blank=True)
    route_text_color = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f"{self.route_short_name} - {self.route_long_name}"

class Stop(models.Model):
    stop_id = models.CharField(max_length=100, unique=True)
    stop_code = models.CharField(max_length=50, null=True, blank=True)
    stop_name = models.CharField(max_length=200)
    stop_desc = models.TextField(null=True, blank=True)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    zone_id = models.CharField(max_length=100, null=True, blank=True)
    stop_url = models.URLField(null=True, blank=True)
    location_type = models.IntegerField(default=0)
    parent_station = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    wheelchair_boarding = models.IntegerField(default=0)

    def __str__(self):
        if self.stop_code:
            return f"{self.stop_name} ({self.stop_code}) - Zone: {self.zone_id}"
        return f"{self.stop_name} - Zone: {self.zone_id}"

    class Meta:
        ordering = ['stop_name']
        verbose_name = 'Bus Stop'
        verbose_name_plural = 'Bus Stops'

class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=100)
    trip_id = models.CharField(max_length=100, unique=True)
    trip_headsign = models.CharField(max_length=200, null=True, blank=True)
    trip_short_name = models.CharField(max_length=50, null=True, blank=True)
    direction_id = models.IntegerField(choices=((0, 'Outbound'), (1, 'Inbound')))
    block_id = models.CharField(max_length=100, null=True, blank=True)
    shape_id = models.CharField(max_length=100, null=True, blank=True)
    wheelchair_accessible = models.IntegerField(default=0)
    bikes_allowed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.route.route_short_name} - {self.trip_headsign}"

class StopTime(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_sequence = models.IntegerField()
    stop_headsign = models.CharField(max_length=200, null=True, blank=True)
    pickup_type = models.IntegerField(default=0)
    drop_off_type = models.IntegerField(default=0)
    shape_dist_traveled = models.FloatField(null=True, blank=True)
    timepoint = models.IntegerField(default=1)

    class Meta:
        ordering = ['trip', 'stop_sequence']

    def __str__(self):
        return f"{self.trip} - {self.stop}"

class FareAttribute(models.Model):
    fare_id = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency_type = models.CharField(max_length=3)
    payment_method = models.IntegerField()
    transfers = models.IntegerField()
    transfer_duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fare_id} - {self.price} {self.currency_type}"

class FareRule(models.Model):
    fare = models.ForeignKey(FareAttribute, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True, blank=True)
    origin_id = models.CharField(max_length=100, null=True, blank=True)
    destination_id = models.CharField(max_length=100, null=True, blank=True)
    contains_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.fare} - {self.route}"

class UserFareHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='origin_fares')
    destination_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='destination_fares')
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    journey_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ))

    def __str__(self):
        return f"{self.user.username} - {self.origin_stop} to {self.destination_stop}"
