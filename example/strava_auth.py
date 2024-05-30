from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class StravaAuthView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        # Your logic here
        return Response({"message": "Received"}, status=200)
    
    def get(self, request, format=None):
        # Your logic here
        return Response({"message": "Received in get"}, status=200)