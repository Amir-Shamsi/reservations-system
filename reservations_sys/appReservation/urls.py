from django.urls import path, include
from rest_framework_nested import routers
from . import views

# Create a router for the ListingViewSet
router = routers.DefaultRouter()
router.register(r'listings', views.ListingViewSet)
urlpatterns = [
    # Include the urls for the ListingViewSet
    path('', include(router.urls)),
]