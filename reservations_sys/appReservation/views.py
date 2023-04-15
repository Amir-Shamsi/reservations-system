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

