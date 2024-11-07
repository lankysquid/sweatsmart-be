import os
import json
from pydantic import BaseModel
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Best practice to load from environment variables

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

class Workout(BaseModel):
    title: str
    plan: str
    

def gpt_workout_details(difficulty, sport) -> Workout:
    user_input = difficulty

    if not user_input:
        return {"error": "No message provided"}

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a coach specializing in endurance athletics for running, cycling, and swimming.\n"
            f"The JSON object must use the schema: {json.dumps(Workout.model_json_schema(), indent=2)}"
        },
        {
            "role": "user",
            "content": f"Using ten words or less plus a title such as 'Tempo Run' or 'Interval Workout', create a {difficulty} {sport} workout that lasts 45 minutes.",
        }
    ],
    model="llama3-8b-8192",
    temperature=0.4,
    max_tokens=1024,
    response_format={"type": "json_object"}
)

    workout_plan = chat_completion.choices[0].message.content
    print(workout_plan)
    return Workout.model_validate_json(workout_plan)


