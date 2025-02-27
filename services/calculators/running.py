from services.gpt.chatbot import gpt_workout_details

def calculate_average_run_pace(strava_stats: dict) -> float:
    """Calculates average pace based on recent run totals."""
    elapsed_time = strava_stats["recent_run_totals"]["elapsed_time"]
    distance = strava_stats["recent_run_totals"]["distance"]
    if elapsed_time == 0 or distance == 0:
        return 0
    # 1609.344 is used to convert meters to miles (for pace calculation)
    average_pace = elapsed_time / (distance / 1609.344)
    return average_pace

def average_pace_readable(pace):
    minutes = round(pace // 60)
    seconds = round(pace % 60)
    return f"{minutes}:{str(seconds).zfill(2)}"


def calculate_average_run_time(strava_stats: dict) -> float:
    """Calculates average workout time based on recent run totals."""
    elapsed_time = strava_stats["recent_run_totals"]["elapsed_time"]
    if elapsed_time == 0:
        return 0
    count = strava_stats["recent_run_totals"]["count"]

    average_time = elapsed_time / count
    return average_time

def calculate_runs(average_pace: float, average_time: float, suggested: str) -> dict:
    if average_time == 0:
        return {"To See Data, Record a Run in Strava"}
    easy_pace = average_pace_readable(average_pace * .95)
    easy_time = average_time * 0.8
    easy_workout_plan = gpt_workout_details("Easy", "running", easy_time)
    easy_title = easy_workout_plan.title
    easy_run = {"pace": easy_pace, "time": easy_time, "suggested": suggested == "EASY", "title": easy_title, "difficulty": "easy", "pace_unit": "mins/mi", "workout_plan": easy_workout_plan.plan} 
    medium_pace = average_pace_readable(average_pace * 0.825)
    medium_time = average_time * 0.9
    medium_workout_plan = gpt_workout_details("Medium", "running", medium_time)
    medium_title = medium_workout_plan.title
    medium_run = {"pace": medium_pace, "time": medium_time, "suggested": suggested == "MEDIUM", "title": medium_title, "difficulty": "medium", "pace_unit": "mins/mi", "workout_plan": medium_workout_plan.plan} 
    hard_pace = average_pace_readable(average_pace * 0.78)
    hard_time = average_time * 1.05
    hard_workout_plan = gpt_workout_details("Difficult", "running", hard_time)
    hard_title = hard_workout_plan.title
    hard_run = {"pace": hard_pace, "time": hard_time, "suggested": suggested == "HARD", "title": hard_title, "difficulty": "hard", "pace_unit": "mins/mi", "workout_plan": hard_workout_plan.plan} 
    return [easy_run, medium_run, hard_run]