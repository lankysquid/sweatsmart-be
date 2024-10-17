def calculate_average_ride_speed(strava_stats: dict) -> float:
    """Calculates average speed based on recent run totals."""
    elapsed_time = strava_stats["recent_ride_totals"]["elapsed_time"]
    if elapsed_time == 0:
        return 0
    distance = strava_stats["recent_ride_totals"]["distance"]

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

def calculate_rides(average_speed: float, average_time: float) -> dict:
    if average_time == 0:
        return {"Go for a ride to see suggested workout"}
    easy_pace = round(average_speed * 0.9)
    easy_time = average_time * 0.8
    suggested = True
    easy_title = "Easy Workout"
    easy_ride = {"pace": easy_pace, "time": easy_time, "suggested": suggested, "title": easy_title, "difficulty": "easy", "pace_unit": "mph"} 
    medium_pace = round(average_speed * 0.95)
    medium_time = average_time * 0.92
    suggested = False
    medium_title = "Medium Workout"
    medium_ride = {"pace": medium_pace, "time": medium_time, "suggested": suggested, "title": medium_title, "difficulty": "medium", "pace_unit": "mph"} 
    hard_pace = round(average_speed * 1.1)
    hard_time = average_time * 1.05
    suggested = False
    hard_title = "Hard Workout"
    hard_ride = {"pace": hard_pace, "time": hard_time, "suggested": suggested, "title": hard_title, "difficulty": "hard", "pace_unit": "mph"} 
    return [easy_ride, medium_ride, hard_ride]