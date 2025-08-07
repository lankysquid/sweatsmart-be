import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from services.strava_stats_service import StravaStatsService
from rest_framework.exceptions import ValidationError, PermissionDenied
from sweat_smart.serializers import StravaStatsRequestSerializer
import requests
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

logger = logging.getLogger(__name__)

class StravaStatsView(APIView):
    """
    View for handling Strava statistics and workout recommendations.
    Business logic is delegated to the service layer and model methods.
    """
    # Only allow logged‐in users with a valid token/session
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Optional: rate‐limit to e.g. 100 requests per user per hour
    throttle_classes = [UserRateThrottle]
    throttle_scope = "strava_stats"
    
    # remove @csrf_exempt from your POST if you still need CSRF protectio
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        """Handle POST requests - placeholder for future functionality."""
        return Response({"message": "Received"}, status=status.HTTP_200_OK)
    
    def get(self, request, format=None):
        """
        Generate workout recommendations based on Strava athlete data.
        
        Query Parameters:
            athlete_id: Strava athlete ID
            access_token: Strava access token
        """
        logger.info(f"Strava stats request from {request.META.get('REMOTE_ADDR')}")
        
        # Use serializer for validation
        serializer = StravaStatsRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {"message": "Invalid request parameters", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        athlete_id = validated_data['athlete_id']
        access_token = validated_data['access_token']
        
        try:
            # Delegate business logic to service layer
            workout_data = StravaStatsService.generate_workout_recommendations(
                athlete_id, access_token
            )
            
            logger.info(f"Successfully generated workouts for athlete {athlete_id}")
            return Response(workout_data, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return Response(
                {"message": "Invalid request parameters", "details": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except PermissionDenied as e:
            logger.warning(f"Permission denied: {e}")
            return Response(
                {"message": "Access denied", "details": str(e)}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        except requests.RequestException as e:
            logger.error(f"Strava API error for athlete {athlete_id}: {e}")
            return Response(
                {"message": "Error communicating with Strava API", "details": str(e)}, 
                status=status.HTTP_502_BAD_GATEWAY
            )
            
        except Exception as e:
            logger.error(f"Unexpected error for athlete {athlete_id}: {e}")
            return Response(
                {"message": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )