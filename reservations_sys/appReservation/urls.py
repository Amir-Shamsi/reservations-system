from django.urls import path, include
from rest_framework_nested import routers
from . import views

# Create a router for the ListingViewSet
router = routers.DefaultRouter()
router.register(r'listings', views.ListingViewSet)
# Create a nested router for the RoomViewSet, nested under the ListingViewSet
listings_router = routers.NestedDefaultRouter(router, r'listings', lookup='listing')
listings_router.register(r'rooms', views.RoomViewSet, basename='listing-rooms')
urlpatterns = [
    # Include the urls for the ListingViewSet
    path('', include(router.urls)),
]