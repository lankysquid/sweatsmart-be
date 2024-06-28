import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dotenv import load_dotenv


strava_auth_url = 'https://www.strava.com/api/v3/oauth/token'

load_dotenv()

class StravaAuthView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        # Your logic here
        return Response({"message": "Received"}, status=200)
    
    def get(self, request, format=None):
        # Your logic here
        code = request.query_params['code']
        STRAVA_CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']
        STRAVA_CLIENT_ID = os.environ['STRAVA_CLIENT_ID']
        params = { 'client_id': STRAVA_CLIENT_ID,
                   'client_secret': STRAVA_CLIENT_SECRET,
                   'code': code,
                   'grant_type': 'authorization_code'}
        response = requests.post(strava_auth_url, params=params)
        return Response(response.json(), status=200)