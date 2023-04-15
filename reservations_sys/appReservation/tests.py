from datetime import datetime
import pytz
from django.template.loader import render_to_string
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Reservation, Room, Listing, User

# Initialize the APIClient
client = APIClient()


class AppReservationTest(TestCase):
    """ Test module for Room Availability API """

    def setUp(self):
        # Sample Listings
        self.listing1 = Listing.objects.create(
            name='Test Listing 1',
            description='Test description 1',
            owner=User.objects.create_user(
                'test1',
                'test1@test.com',
                'testpassword',
                is_staff=True
            )
        )

        self.listing2 = Listing.objects.create(
            name='Test Listing 2',
            description='Test description 2',
            owner=User.objects.create_user(
                'test2',
                'test2@test.com',
                'testpassword',
                is_staff=True
            )
        )

        # Sample Rooms
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

        # Sample Reservations
        self.reservation1 = Reservation.objects.create(
            room=self.room3,
            name='John Doe',
            start_time=datetime(2023, 11, 15, 11, 30, 0, 0, tzinfo=pytz.UTC),
            end_time=datetime(2023, 12, 17, 12, 0, 0, 0, tzinfo=pytz.UTC)
        )

        self.reservation2 = Reservation.objects.create(
            room=self.room2,
            name='Jane Smith',
            start_time=datetime(2023, 4, 17, 14, 45, 0, 0, tzinfo=pytz.UTC),
            end_time=datetime(2023, 4, 20, 12, 0, 0, 0, tzinfo=pytz.UTC)
        )

    def test_get_listings(self):
        url = '/listings/'

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)

    def test_get_listing_available_rooms(self):
        # Test to get available rooms for a listing
        url = f'/listings/{self.listing1.pk}/rooms/'

        response = client.post(
            url,
            {
                'start_time':
                    datetime(2023, 4, 20, 0, 0, 0, 0, tzinfo=pytz.UTC),
                'end_time':
                    datetime(2023, 4, 25, 12, 0, 0, 0, tzinfo=pytz.UTC)
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_get_available_rooms(self):
        # Test to get available rooms for a listing
        url = '/rooms/list/'

        response = client.post(
            url,
            {
                'start_time':
                    datetime(2023, 4, 20, 0, 0, 0, 0, tzinfo=pytz.UTC),

                'end_time':
                    datetime(2023, 4, 25, 12, 0, 0, 0, tzinfo=pytz.UTC)
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_create_reservation(self):
        # Test to create a reservation for a room
        url = f'/listings/{self.listing1.pk}/rooms/{self.room1.pk}/reserve/'

        data = {
            'name': 'Test Reservation',
            'start_time': '2023-04-20T12:00:00Z',
            'end_time': '2023-04-25T12:00:00Z'
        }

        response = client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Reservation')

    def test_create_reservation_conflict(self):
        # Test to create a reservation for a room with conflicting time
        url = f'/listings/{self.listing1.pk}/rooms/{self.room1.pk}/reserve/'

        data = {
            'name': 'Test Reservation',
            'start_time': '2023-04-22T12:00:00Z',
            'end_time': '2023-04-23T12:00:00Z'
        }

        # Create a reservation with conflicting time first
        Reservation.objects.create(
            room=self.room1,
            name='Test Reservation Conflict',
            start_time='2023-04-21T12:00:00Z',
            end_time='2023-04-24T12:00:00Z'
        )

        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_booked_rooms_text(self):
        url = '/booked-rooms/text/'

        # Loging as listing owner
        self.client.login(username='test2', password='testpassword')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn(
            f"Room {self.reservation1.room.room_number}:"
            f" {self.reservation1.name} "
            f"({self.reservation1.start_time.strftime('%Y-%m-%d %H:%M')} - "
            f"{self.reservation1.end_time.strftime('%Y-%m-%d %H:%M')})",
            response.content.decode())

    def test_booked_rooms_html(self):
        url = '/booked-rooms/html/'
        # Loging as listing owner
        self.client.login(username='test2', password='testpassword')

        response = self.client.get(url)

        # Check response status code and content type
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'text/html')

        # Check response content
        expected_html = render_to_string('report/booked_rooms.html',
                                         {'reservations': [self.reservation1],
                                          'listing': self.listing2.name})

        self.maxDiff = None
        self.assertMultiLineEqual(response.content.decode(), expected_html)
