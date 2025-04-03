import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dotenv import load_dotenv

load_dotenv()

strava_auth_url = 'https://www.strava.com/api/v3/oauth/token'
strava_url = 'https://www.strava.com/api/v3/'
STRAVA_CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']
STRAVA_CLIENT_ID = os.environ['STRAVA_CLIENT_ID']

def get_strava_athlete(access_token):
    athlete_url = strava_url + f'athlete'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    print(headers)
    print(athlete_url)
    response = requests.get(athlete_url, headers=headers)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~FART~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print(response.json())
    response = response.json()
    return response


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
        print ("In strava_auth")
        print(f"request: {request}")
        code = request.query_params.get('code')
        refresh_token = request.query_params.get('refresh_token')
        
        if code:
            params = build_code_params(code)
            print("sending code params", params)
        elif refresh_token:
            params = build_refresh_params(refresh_token)
            print("sending refresh token", params)
        else:
            return Response({"message": "Invalid request"}, status=400)
        response = requests.post(strava_auth_url, params=params)
        print(response.json())
        
        if response.status_code != 200:
            return Response({"message": "Error from Strava API", "details": response.json()}, status=response.status_code)
            
        athlete = get_strava_athlete(response.json()["access_token"])
        return Response(response.json(), status=200)