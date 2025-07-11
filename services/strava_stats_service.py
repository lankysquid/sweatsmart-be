import logging
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, PermissionDenied

logger = logging.getLogger(__name__)

User = get_user_model()

class StravaStatsService:
    """Service layer for handling Strava stats operations."""
    
    @staticmethod
    def get_athlete_by_strava_credentials(athlete_id, access_token):
        """
        Retrieve athlete by Strava ID and validate access token.
        
        Args:
            athlete_id (str): The Strava athlete ID
            access_token (str): The Strava access token
            
        Returns:
            User: The authenticated user
            
        Raises:
            ValidationError: If credentials are missing
            PermissionDenied: If user not found or token mismatch
        """
        if not athlete_id or not access_token:
            raise ValidationError("Both athlete_id and access_token are required")
        
        try:
            athlete = User.objects.get(strava_id=athlete_id)
        except User.DoesNotExist:
            logger.warning(f"Athlete with Strava ID {athlete_id} not found")
            raise PermissionDenied("Athlete not found")
        
        # Validate access token matches (basic security check)
        if athlete.strava_access_token != access_token:
            logger.warning(f"Access token mismatch for athlete {athlete_id}")
            raise PermissionDenied("Invalid access token")
        
        return athlete
    
    @staticmethod
    def generate_workout_recommendations(athlete_id, access_token):
        """
        Generate workout recommendations for an athlete.
        
        Args:
            athlete_id (str): The Strava athlete ID
            access_token (str): The Strava access token
            
        Returns:
            dict: Workout recommendations data
        """
        athlete = StravaStatsService.get_athlete_by_strava_credentials(
            athlete_id, access_token
        )
        
        return athlete.generate_workout_recommendations()
