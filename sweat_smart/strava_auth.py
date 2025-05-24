import os
import requests
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dotenv import load_dotenv
from sweat_smart.athletes.views import get_strava_athlete, create


load_dotenv()

logger = logging.getLogger(__name__)

strava_auth_url = 'https://www.strava.com/api/v3/oauth/token'
strava_url = 'https://www.strava.com/api/v3/'
STRAVA_CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']
STRAVA_CLIENT_ID = os.environ['STRAVA_CLIENT_ID']

def build_code_params(code):
    return { 'client_id': STRAVA_CLIENT_ID,
             'client_secret': STRAVA_CLIENT_SECRET,
             'code': code,
             'grant_type': 'authorization_code'}
    
def build_refresh_params(refresh_token):
    return { 'client_id': STRAVA_CLIENT_ID,
             'client_secret': STRAVA_CLIENT_SECRET,
             'refresh_token': refresh_token,
             'grant_type': 'refresh_token'}
class StravaAuthView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        return Response({"message": "Received"}, status=200)
    
    def get(self, request, format=None):
        logger.info("In strava_auth")
        logger.info(f"request: {request}")
        code = request.query_params.get('code')
        refresh_token = request.query_params.get('refresh_token')
        
        if code:
            params = build_code_params(code)
            logger.info(f"sending code params {params}")
        elif refresh_token:
            params = build_refresh_params(refresh_token)
            logger.info(f"sending refresh token {params}")
        else:
            return Response({"message": "Invalid request"}, status=400)
        response = requests.post(strava_auth_url, params=params)
        logger.info("~~~~~~~~~~~~~~~~~~~~~~~~~~FART~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


        athlete_tokens = response.json()
        
        if response.status_code != 200:
            return Response({"message": "Error from Strava API", "details": response.json()}, status=response.status_code)
            
        athlete = get_strava_athlete(response.json()["access_token"])
        create(athlete, athlete_tokens)
        return Response(response.json(), status=200)