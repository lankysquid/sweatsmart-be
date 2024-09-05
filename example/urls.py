# example/urls.py
from django.urls import path

from example.views import index

from example.strava_auth import StravaAuthView
from example.strava_stats import StravaStatsView

urlpatterns = [
    path('', index),
    path('strava_auth', StravaAuthView.as_view(), name='strava_auth'),
    path('strava_stats', StravaStatsView.as_view(), name='strava_stats'),
]