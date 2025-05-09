from services.calculators.running import average_pace_readable
from services.gpt.chatbot import gpt_workout_details

def calculate_average_swim_pace(strava_stats: dict) -> float:
    """Calculates average pace based on recent run totals."""
    elapsed_time = strava_stats["recent_swim_totals"]["elapsed_time"]
    distance = strava_stats["recent_swim_totals"]["distance"]
    if elapsed_time == 0 or distance == 0:
        return 0
    # 1609.344 is used to convert meters to miles (for pace calculation)
    average_pace = elapsed_time / ((distance * 1.09361) / 100)
    return average_pace


def calculate_average_swim_time(strava_stats: dict) -> float:
    """Calculates average workout time based on recent run totals."""
    elapsed_time = strava_stats["recent_swim_totals"]["elapsed_time"]
    if elapsed_time == 0:
        return 0
    count = strava_stats["recent_swim_totals"]["count"]

    average_time = elapsed_time / count
    return average_time

def calculate_swims(average_pace: float, average_time: float, suggested: str) -> dict:
    if average_time == 0:
        return {"Go for a swim to see data"}
    easy_pace = average_pace_readable(average_pace * 1.05)
    easy_time = average_time * 0.8
    easy_workout_plan = gpt_workout_details("Easy", "swimming", easy_time, easy_pace, "min/100yd")
    easy_title = easy_workout_plan.title
    easy_swim = {"pace": easy_pace, "time": easy_time, "suggested": suggested == "EASY", "title": easy_title, "difficulty": "easy", "pace_unit": "mins/100yd", "workout_plan": easy_workout_plan.plan} 
   
    medium_pace = average_pace_readable(average_pace * 0.95)
    medium_time = average_time * 0.92
    medium_workout_plan = gpt_workout_details("Medium", "swimming", medium_time, medium_pace, "min/100yd")
    medium_title = medium_workout_plan.title
    medium_swim = {"pace": medium_pace, "time": medium_time, "suggested": suggested == "MEDIUM", "title": medium_title, "difficulty": "medium", "pace_unit": "mins/100yd", "workout_plan": medium_workout_plan.plan} 
    
    hard_pace = average_pace_readable(average_pace * 0.9)
    hard_time = average_time * 1.05
    hard_workout_plan = gpt_workout_details("Hard", "swimming", hard_time, hard_pace, "min/100yd")
    hard_title = hard_workout_plan.title
    hard_swim = {"pace": hard_pace, "time": hard_time, "suggested": suggested == "HARD", "title": hard_title, "difficulty": "hard", "pace_unit": "mins/100yd", "workout_plan": hard_workout_plan.plan} 
    return [easy_swim, medium_swim, hard_swim]