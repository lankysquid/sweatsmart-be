# example/urls.py
from django.urls import path

from example.views import index

from example.strava_auth import StravaAuthView

urlpatterns = [
    path('', index),
    path('strava_auth', StravaAuthView.as_view(), name='strava_auth'),
]