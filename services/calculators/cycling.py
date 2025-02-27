from services.gpt.chatbot import gpt_workout_details

def calculate_average_ride_speed(strava_stats: dict) -> float:
    """Calculates average speed based on recent run totals."""
    elapsed_time = strava_stats["recent_ride_totals"]["elapsed_time"]
    distance = strava_stats["recent_ride_totals"]["distance"]
    if elapsed_time == 0 or distance == 0:
        return 0
    # 1609.344 is used to convert meters to miles (for speed calculation)
    average_pace = elapsed_time / (distance / 1609.344)
    average_speed = 60 / (average_pace / 60)
    return average_speed


def calculate_average_ride_time(strava_stats: dict) -> float:
    """Calculates average workout time based on recent run totals."""
    elapsed_time = strava_stats["recent_ride_totals"]["elapsed_time"]
    if elapsed_time == 0:
        return 0
    count = strava_stats["recent_ride_totals"]["count"]

    average_time = elapsed_time / count
    return average_time

def calculate_rides(average_speed: float, average_time: float, suggested: str) -> dict:
    if average_time == 0:
        return {"Go for a ride to see suggested workout"}
   
    easy_pace = round(average_speed)
    easy_time = average_time * 0.85
    easy_workout_plan = gpt_workout_details("Easy", "cycling")
    easy_title = easy_workout_plan.title
    easy_ride = {"pace": easy_pace, "time": easy_time, "suggested": suggested == 'EASY', "title": easy_title, "difficulty": "easy", "pace_unit": "mph", "workout_plan": easy_workout_plan.plan} 
   
    medium_pace = round(average_speed * 1.15)
    medium_time = average_time
    medium_workout_plan = gpt_workout_details("Medium", "cycling")
    medium_title = medium_workout_plan.title
    medium_ride = {"pace": medium_pace, "time": medium_time, "suggested": suggested == 'MEDIUM', "title": medium_title, "difficulty": "medium", "pace_unit": "mph", "workout_plan": medium_workout_plan.plan} 
   
    hard_pace = round(average_speed * 1.20)
    hard_time = average_time * 1.1
    hard_workout_plan = gpt_workout_details("Hard", "cycling")
    hard_title = hard_workout_plan.title
    hard_ride = {"pace": hard_pace, "time": hard_time, "suggested": suggested == 'HARD', "title": hard_title, "difficulty": "hard", "pace_unit": "mph", "workout_plan": hard_workout_plan.plan} 
    
    return [easy_ride, medium_ride, hard_ride]

# def calculate_suggested_workout()