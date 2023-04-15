import datetime
from datetime import datetime
import pytz
from django.template.loader import render_to_string
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import *
from .serializers import *

# Initialize the APIClient
client = APIClient()


class AppReservationTest(TestCase):
    """ Test module for Room Availability API """

    def setUp(self):
        self.listing1 = Listing.objects.create(
            name='Test Listing 1',
            description='Test description 1',
            owner=User.objects.create_user('test1', 'test1@test.com', 'testpassword', is_staff=True)
        )
        self.listing2 = Listing.objects.create(
            name='Test Listing 2',
            description='Test description 2',
            owner=User.objects.create_user('test2', 'test2@test.com', 'testpassword', is_staff=True)
        )
        self.room1 = Room.objects.create(
            listing=self.listing1,
            room_number=101,
            price_per_night=300,
        )
        self.room2 = Room.objects.create(
            listing=self.listing1,
            room_number=102,
            price_per_night=600,
        )
        self.room3 = Room.objects.create(
            listing=self.listing2,
            room_number=201,
            price_per_night=900,
        )
        self.reservation1 = Reservation.objects.create(room=self.room3, name='John Doe',
                                                       start_time=datetime(2023, 11, 15, 11, 30, 0, 0, tzinfo=pytz.UTC),
                                                       end_time=datetime(2023, 12, 17, 12, 0, 0, 0, tzinfo=pytz.UTC))
        self.reservation2 = Reservation.objects.create(room=self.room2, name='Jane Smith',
                                                       start_time=datetime(2023, 4, 17, 14, 45, 0, 0, tzinfo=pytz.UTC),
                                                       end_time=datetime(2023, 4, 20, 12, 0, 0, 0, tzinfo=pytz.UTC))

    def test_get_listings(self):
        url = f'/listings/'
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)
