from django.urls import path

from backend_taxi_app.trips.api.views import (
    TripView,
    PayView
)

app_name = "trips"
urlpatterns = [
    path('trip/<uuid:trip_id>/', TripView.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='trip_detail'),
    path('trip/<uuid:trip_id>/pay/',
         PayView.as_view({'patch': 'partial_update'}), name='trip_payment'),
]
