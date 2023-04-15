from django.utils import timezone
from rest_framework import serializers
from .models import Room, Reservation, Listing


# Define Reservation serializer
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['name', 'start_time', 'end_time']

    # Validate reservation times
    def validate(self, data):
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError(
                'Reservation end time must exceeds the start time.'
            )

        if data['start_time'] < timezone.now():
            raise serializers.ValidationError(
                'Start time cannot be before the current time.'
            )

        return data


# Define Room serializer
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'price_per_night', 'listing']


# Define Room availability serializer
class RoomAvailabilitySerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()


# Define Listing serializer
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'name']
