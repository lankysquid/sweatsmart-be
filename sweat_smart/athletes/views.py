import requests
from django.contrib.auth import get_user_model, login
from django.utils import timezone
from datetime import datetime

Athlete = get_user_model()

strava_url = 'https://www.strava.com/api/v3/'

def get_strava_athlete(access_token):
    athlete_url = strava_url + f'athlete'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    print(headers)
    print(athlete_url)
    response = requests.get(athlete_url, headers=headers)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~FART~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(response.json())
    response = response.json()
    return response
  
def create(data, athlete_tokens):
    strava_id = data['id']
    expires_at = timezone.make_aware(datetime.fromtimestamp(athlete_tokens['expires_at']))
    
    athlete, created = Athlete.objects.update_or_create(
        strava_id=strava_id,
        defaults={
            'first_name': data.get('firstname', ''),
            'last_name': data.get('lastname', ''),
            'profile_picture': data.get('profile_medium', ''),
            'access_token': athlete_tokens['access_token'],
            'refresh_token': athlete_tokens['refresh_token'],
            'strava_token_expires_at': expires_at,
        }
    )