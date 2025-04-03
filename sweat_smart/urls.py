# sweat_smart/urls.py
from django.urls import path

from sweat_smart.views import index

from sweat_smart.strava_auth import StravaAuthView
from sweat_smart.strava_stats import StravaStatsView

urlpatterns = [
    path('', index),
    path('strava_auth', StravaAuthView.as_view(), name='strava_auth'),
    path('strava_stats', StravaStatsView.as_view(), name='strava_stats'),
]