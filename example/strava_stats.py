import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dotenv import load_dotenv
from services.calculators.running import calculate_average_run_time, calculate_average_run_pace, calculate_runs
from services.calculators.cycling import calculate_average_ride_speed, calculate_average_ride_time, calculate_rides
from services.calculators.swimming import calculate_average_swim_pace, calculate_average_swim_time, calculate_swims
from services.gpt.chatbot import gpt_workout_details 

load_dotenv()

strava_url = 'https://www.strava.com/api/v3/'
STRAVA_CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']
STRAVA_CLIENT_ID = os.environ['STRAVA_CLIENT_ID']

def get_stats(strava_stats: dict) -> dict:
    print("=====================fart=====================")
    workout_plan = gpt_workout_details("")
    average_ride_pace = calculate_average_ride_speed(strava_stats)
    average_ride_time = calculate_average_ride_time(strava_stats)
    rides = calculate_rides(average_ride_pace, average_ride_time)
    average_run_pace = calculate_average_run_pace(strava_stats)
    average_run_time = calculate_average_run_time(strava_stats)
    runs = calculate_runs(average_run_pace, average_run_time)
    average_swim_pace = calculate_average_swim_pace(strava_stats)
    average_swim_time = calculate_average_swim_time(strava_stats)
    swims = calculate_swims(average_swim_pace, average_swim_time)
    return {"rides": rides, "runs": runs, "swims": swims}

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
        print(response)
        
        if response.status_code >= 400:
            return Response({"message": "Error from Strava API", "details": response.json()}, status=response.status_code)
        
        workouts = get_stats(response.json())
        
        print('workouts', workouts)
        
        return Response({"workouts": workouts}, status=200)