from django.urls import path, include
from rest_framework_nested import routers
from . import views

# Create a router for the ListingViewSet
router = routers.DefaultRouter()
router.register(r'listings', views.ListingViewSet)

# Create a nested router for the RoomViewSet, nested under the ListingViewSet
listings_router = routers.NestedDefaultRouter(router, r'listings', lookup='listing')
listings_router.register(r'rooms', views.RoomViewSet, basename='listing-rooms')

# Create a router for the RoomViewSet, not nested under any other view set
rooms_router = routers.DefaultRouter()
rooms_router.register(r'list', views.RoomViewSet, basename='rooms-list')

# Create a nested router for the ReservationViewSet, nested under the RoomViewSet, which is nested under the ListingViewSet
reservation_router = routers.NestedDefaultRouter(listings_router, r'rooms', lookup='room')
reservation_router.register(r'reserve', views.ReservationViewSet, basename='reserve')

# Define urlpatterns for the API views
urlpatterns = [
    # Include the urls for the ListingViewSet
    path('', include(router.urls)),
    # Include the urls for the RoomViewSet nested under the ListingViewSet
    path('', include(listings_router.urls)),
    # Include the urls for the ReservationViewSet nested under the RoomViewSet, which is nested under the ListingViewSet
    path('', include(reservation_router.urls)),
    # Include the urls for the RoomViewSet not nested under any other view set
    path('rooms/', include(rooms_router.urls)),
    # View for generating an HTML report of booked rooms for the logged in user's listings
    path('booked-rooms/html/', views.BookedRoomsHTML.as_view(), name='booked_rooms_html'),
]