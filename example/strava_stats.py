import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dotenv import load_dotenv
from services.calculators.running import calculate_average_run_time, calculate_average_run_pace, calculate_suggested_runs

load_dotenv()

strava_url = 'https://www.strava.com/api/v3/'
STRAVA_CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']
STRAVA_CLIENT_ID = os.environ['STRAVA_CLIENT_ID']

class StravaStatsView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        return Response({"message": "Received"}, status=200)
    
    def get(self, request, format=None):
        athlete_id = request.query_params.get('athlete_id')
        access_token = request.query_params.get('access_token')
        url = strava_url + f'athletes/{athlete_id}/stats'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        print(headers)
        print(url)
        response = requests.get(url, headers=headers)
        average_run_pace = calculate_average_run_pace(response.json())
        average_run_time = calculate_average_run_time(response.json())
        suggested_runs = calculate_suggested_runs(average_run_pace, average_run_time)
        print(suggested_runs)

        print(response)
        if response.status_code != 200:
            return Response({"message": "Error from Strava API", "details": response.json()}, status=response.status_code)
        
        return Response({"easy_run":suggested_runs[0], "medium_run":suggested_runs[1], "hard_run":suggested_runs[2]}, status=200)