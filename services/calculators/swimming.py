def calculate_average_swim_pace(strava_stats: dict) -> float:
    """Calculates average pace based on recent run totals."""
    elapsed_time = strava_stats["recent_swim_totals"]["elapsed_time"]
    if elapsed_time == 0:
        return 0
    distance = strava_stats["recent_swim_totals"]["distance"]

    # 1609.344 is used to convert meters to miles (for pace calculation)
    average_pace = elapsed_time / (distance / 1609.344)
    return average_pace


def calculate_average_swim_time(strava_stats: dict) -> float:
    """Calculates average workout time based on recent run totals."""
    elapsed_time = strava_stats["recent_swim_totals"]["elapsed_time"]
    if elapsed_time == 0:
        return 0
    count = strava_stats["recent_swim_totals"]["count"]

    average_time = elapsed_time / count
    return average_time

def calculate_swims(average_pace: float, average_time: float) -> dict:
    if average_time == 0:
        return {"Go for a swim to see data"}
    easy_pace = average_pace * 1.05
    easy_time = average_time * 0.8
    suggested = True
    easy_title = "Easy Workout"
    easy_swim = {"pace": easy_pace, "time": easy_time, "suggested": suggested, "title": easy_title, "difficulty": "easy"} 
    medium_pace = average_pace * 0.95
    medium_time = average_time * 0.92
    suggested = False
    medium_title = "Medium Workout"
    medium_swim = {"pace": medium_pace, "time": medium_time, "suggested": suggested, "title": medium_title, "difficulty": "medium"} 
    hard_pace = average_pace * 0.9
    hard_time = average_time * 1.05
    suggested = False
    hard_title = "Hard Workout"
    hard_swim = {"pace": hard_pace, "time": hard_time, "suggested": suggested, "title": hard_title, "difficulty": "hard"} 
    return [easy_swim, medium_swim, hard_swim]