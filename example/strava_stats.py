import os
import requests
# from pprint import pprint
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

def get_stats(strava_stats: dict, strava_activities: dict) -> dict:
    print("=====================fart=====================")
    print(strava_activities[0]["kilojoules"])
    print(len(strava_activities))
    kilojoules_array = [] 
    for activity in strava_activities[:10]:
        if activity.get('kilojoules'):
            # pprint(activity["kilojoules"], indent=4)
            kilojoules_array.append(activity["kilojoules"])
    average_kjs = (sum(kilojoules_array) / len(kilojoules_array))
    recent_kjs = kilojoules_array[0]
    print(recent_kjs)
    print(average_kjs)
    suggested = ''
    if average_kjs > recent_kjs:
        suggested = 'HARD'
    elif average_kjs == recent_kjs:
        suggested = 'MEDIUM'
    elif average_kjs < recent_kjs:
        suggested = 'EASY'
    average_ride_pace = calculate_average_ride_speed(strava_stats)
    average_ride_time = calculate_average_ride_time(strava_stats)
    rides = calculate_rides(average_ride_pace, average_ride_time, suggested)
    average_run_pace = calculate_average_run_pace(strava_stats)
    average_run_time = calculate_average_run_time(strava_stats)
    runs = calculate_runs(average_run_pace, average_run_time, suggested)
    average_swim_pace = calculate_average_swim_pace(strava_stats)
    average_swim_time = calculate_average_swim_time(strava_stats)
    swims = calculate_swims(average_swim_pace, average_swim_time, suggested)
    return {"rides": rides, "runs": runs, "swims": swims}

class StravaStatsView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        return Response({"message": "Received"}, status=200)
    
    def get(self, request, format=None):
        print(f"in strava_stats {request}")
        athlete_id = request.query_params.get('athlete_id')
        access_token = request.query_params.get('access_token')
        stats_url = strava_url + f'athletes/{athlete_id}/stats'
        activities_url = strava_url + f'athlete/activities'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        print(headers)
        print(stats_url)
        print(activities_url)
        strava_stats = requests.get(stats_url, headers=headers)
        strava_activities = requests.get(activities_url, headers=headers)
        # print(strava_stats)
        # print(strava_activities.json())
        
        if strava_stats.status_code >= 400:
            return Response({"message": "Error from Strava API", "details": strava_stats.json()}, status=strava_stats.status_code)
        
        workouts = get_stats(strava_stats.json(), strava_activities.json())
        
        # pprint(f'workouts {workouts}', indent=2)
        
        return Response({"workouts": workouts}, status=200)