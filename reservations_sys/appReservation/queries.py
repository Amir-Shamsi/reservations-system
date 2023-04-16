from .models import Reservation, Room
from django.db.models import Q


def is_reservation_exists(start_time, end_time, room):
    Reservation.objects.filter(
        room=room,
        start_time__lt=end_time,
        end_time__gt=start_time
    ).exists()


def get_available_rooms(start_time, end_time, listing_pk=None):
    """
    Returns the list of available rooms for the given time range.
    If a listing_pk is provided, filters the queryset by that ID.
    """
    queryset = Room.objects.filter(
        ~Q(
            reservation__start_time__lt=end_time,
            reservation__end_time__gt=start_time
        )
    )

    """
        If a listing ID was provided in the URL, filter the queryset by that ID
    """
    if listing_pk:
        queryset = queryset.filter(listing_id=listing_pk)

    return queryset
