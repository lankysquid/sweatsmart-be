# example/views.py
from datetime import datetime

from django.http import HttpResponse

import json

def index(request):
    now = datetime.now()
    # html = f'''
    # <html>
    #     <body>
    #         <h1>Hello from Vercel!</h1>
    #         <p>The current time is { now }.</p>
    #     </body>
    # </html>
    # '''
    json_data = {
        "message": "Hello from Vercel!",
        "time": now
    }
    return HttpResponse(json.dumps(json_data), content_type='application/json')