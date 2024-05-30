# example/views.py
from datetime import datetime

from django.http import HttpResponse

import json

def index(request):
    now = datetime.now()
    json_data = {
        "message": "Hello from Vercel!",
        "time": str(now)
    }
    return HttpResponse(json.dumps(json_data), content_type='application/json')

