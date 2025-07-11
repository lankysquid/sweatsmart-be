from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import os
import requests
import logging
from services.calculators.running import calculate_average_run_time, calculate_average_run_pace, calculate_runs
from services.calculators.cycling import calculate_average_ride_speed, calculate_average_ride_time, calculate_rides
from services.calculators.swimming import calculate_average_swim_pace, calculate_average_swim_time, calculate_swims

logger = logging.getLogger(__name__)

class CustomUserManager(BaseUserManager):
    """Manager for CustomUser with email-based authentication"""
    
    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email instead of username"""
    
    strava_id = models.IntegerField()
    email = models.EmailField(null=True, unique=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    strava_refresh_token = models.CharField(max_length=200, blank=True)
    strava_access_token = models.CharField(max_length=200, blank=True)
    strava_token_expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    
    class Meta:
        constraints = [
            # Ensure either email or strava_id is provided
            models.CheckConstraint(
                check=models.Q(email__isnull=False) | models.Q(strava_id__isnull=False),
                name='either_email_or_strava_required'
            )
        ]

    def __str__(self):
        return self.email
    
    def get_strava_headers(self):
        """Generate authorization headers for Strava API requests."""
        return {'Authorization': f'Bearer {self.strava_access_token}'}
    
    def fetch_strava_stats(self):
        """Fetch athlete stats from Strava API."""
        if not self.strava_access_token:
            raise ValueError("No Strava access token available")
        
        strava_url = 'https://www.strava.com/api/v3/'
        stats_url = f"{strava_url}athletes/{self.strava_id}/stats"
        headers = self.get_strava_headers()
        
        response = requests.get(stats_url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def fetch_strava_activities(self, limit=10):
        """Fetch recent activities from Strava API."""
        if not self.strava_access_token:
            raise ValueError("No Strava access token available")
        
        strava_url = 'https://www.strava.com/api/v3/'
        activities_url = f"{strava_url}athlete/activities"
        headers = self.get_strava_headers()
        
        response = requests.get(activities_url, headers=headers)
        response.raise_for_status()
        return response.json()[:limit]
    
    def calculate_workout_intensity_suggestion(self, activities):
        """Calculate suggested workout intensity based on recent kilojoules."""
        if not activities:
            return 'MEDIUM'
        
        kilojoules_array = []
        for activity in activities:
            if activity.get('kilojoules'):
                kilojoules_array.append(activity['kilojoules'])
        
        if not kilojoules_array:
            return 'MEDIUM'
        
        average_kjs = sum(kilojoules_array) / len(kilojoules_array)
        recent_kjs = kilojoules_array[0]
        
        if average_kjs > recent_kjs:
            return 'HARD'
        elif average_kjs == recent_kjs:
            return 'MEDIUM'
        else:
            return 'EASY'
    
    def generate_workout_recommendations(self):
        """Generate workout recommendations based on Strava data."""
        try:
            strava_stats = self.fetch_strava_stats()
            strava_activities = self.fetch_strava_activities()
            
            suggested_intensity = self.calculate_workout_intensity_suggestion(strava_activities)
            
            # Calculate rides
            average_ride_pace = calculate_average_ride_speed(strava_stats)
            average_ride_time = calculate_average_ride_time(strava_stats)
            rides = calculate_rides(average_ride_pace, average_ride_time, suggested_intensity)
            
            # Calculate runs
            average_run_pace = calculate_average_run_pace(strava_stats)
            average_run_time = calculate_average_run_time(strava_stats)
            runs = calculate_runs(average_run_pace, average_run_time, suggested_intensity)
            
            # Calculate swims
            average_swim_pace = calculate_average_swim_pace(strava_stats)
            average_swim_time = calculate_average_swim_time(strava_stats)
            swims = calculate_swims(average_swim_pace, average_swim_time, suggested_intensity)
            
            # Get recent workout type
            recent_workout_type = strava_activities[0]["type"] if strava_activities else None
            
            return {
                "workouts": {
                    "rides": rides,
                    "runs": runs,
                    "swims": swims
                },
                "recent_workout_type": recent_workout_type
            }
            
        except requests.RequestException as e:
            logger.error(f"Error fetching Strava data for user {self.id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating workout recommendations for user {self.id}: {e}")
            raise

class AthleteManager(BaseUserManager):
    def create_user(self, email=None, password=None, strava_id=None, **extra_fields):
        # Require either email or strava_id
        if not email and not strava_id:
            raise ValueError('Either email or Strava ID is required')
           
        # Create a new user instance
        user = self.model(
            email=self.normalize_email(email) if email else None,
            strava_id=strava_id,
            **extra_fields
        )
       
        # Handle password
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
           
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
       
        if not email:
            raise ValueError('Email is required for superusers')
           
        return self.create_user(email=email, password=password, **extra_fields)

