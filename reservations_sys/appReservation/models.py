from django.contrib.auth.models import User
from django.db import models

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Room(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50)
    room_number = models.CharField(max_length=10, unique=True)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.listing.name} - {self.room_type}"


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.room.listing.name} - {self.room.room_type}"
