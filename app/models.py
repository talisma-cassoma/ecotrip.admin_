from django.db import models
from django.utils import timezone
import uuid

# Enums como choices
class Role(models.TextChoices):
    PASSENGER = 'passenger', 'Passenger'
    DRIVER = 'driver', 'Driver'

class DriverStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    ON_TRIP = 'on_trip', 'On Trip'
    OFFLINE = 'offline', 'Offline'

class TripStatus(models.TextChoices):
    REQUESTED = 'requested', 'Requested'
    ACCEPTED = 'accepted', 'Accepted'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


# Coord
class Coord(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return f"{self.lat}, {self.lng}"


# Place
class Place(models.Model):
    name = models.CharField(max_length=255)
    location = models.OneToOneField(Coord, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# User
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices)
    image = models.URLField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Refresh Token
class UserRefreshToken(models.Model):
    token = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="refresh_token")
    is_revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.name}"


# Driver
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    car_model = models.CharField(max_length=255)
    car_plate = models.CharField(max_length=50)
    car_color = models.CharField(max_length=50)
    license_number = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    completed_rides = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=DriverStatus.choices)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name


# Trip
class Trip(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    source = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="trips_source")
    destination = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="trips_destination")
    distance = models.FloatField()
    duration = models.FloatField()
    freight = models.FloatField()
    directions = models.JSONField()
    status = models.CharField(max_length=20, choices=TripStatus.choices)

    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="passenger_trips")
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name="driver_trips")

    interested_drivers = models.ManyToManyField(Driver, blank=True, related_name="interested_trips")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip {self.token}"


# Trip Cancellation
class TripCancellation(models.Model):
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, related_name="cancellation")
    cancelled_by = models.CharField(max_length=20, choices=Role.choices)
    reason = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="canceled_trips")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cancellation for {self.trip.token}"


# Point (Driver location points)
class Point(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="points")
    location = models.OneToOneField(Coord, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Point for {self.driver.user.name}"
