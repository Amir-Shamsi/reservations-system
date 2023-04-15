from django.utils import timezone
from rest_framework import serializers
from .models import Room, Reservation, Listing


# Define Room serializer
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'price_per_night', 'listing']


