# Importing necessary modules
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .paginations import Pagination
from .serializers import ListingSerializer, ReservationSerializer, RoomAvailabilitySerializer
from django.db.models import Q
from .models import *
from .serializers import RoomSerializer


# ViewSet for Listing
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    pagination_class = Pagination


# ViewSet to get Rooms
class RoomViewSet(viewsets.ModelViewSet):
    pagination_class = Pagination

    def get_queryset(self):
        # Get the listing ID from the URL, if it exists
        listing_pk = self.kwargs.get('listing_pk')
        if listing_pk:
            queryset = Room.objects.filter(listing_id=listing_pk)
        else:
            queryset = Room.objects.all()

        return get_list_or_404(queryset)

    def create(self, request, *args, **kwargs):
        # Validate input data and get start_time and end_time
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        # Get the list of available rooms for the given time range
        queryset = Room.objects.filter(~Q(reservation__start_time__lt=end_time, reservation__end_time__gt=start_time))

        # If a listing ID was provided in the URL, filter the queryset by that ID
        listing_pk = self.kwargs.get('listing_pk')
        if listing_pk:
            queryset = queryset.filter(listing_id=self.kwargs['listing_pk'])

        # Serialize the queryset and return the response
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        # Return a different serializer class depending on the request method
        if self.request.method == 'GET':
            return RoomSerializer
        elif self.request.method == 'POST':
            return RoomAvailabilitySerializer
        else:
            return super().get_serializer_class()

