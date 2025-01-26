import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate
from setup.utils.jwt_utils import JWTUtils

class TokenView(View):
    """
    API View to get a JWT token using username and password.
    """
    def post(self, request, *args, **kwargs):     
        body = json.load(request)
        username = body['username']
        password = body['password']

        if not username or not password:
            return JsonResponse({
                "error": "Username and password are required"
            }, status=400)

       
        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({
                "error": "Invalid credentials"
            }, status=401)

     
        payload = {
            "user_id": user.id,
            "username": user.username
        }
        token = JWTUtils.encode(payload)

        return JsonResponse({
            "message": "Token generated successfully",
            "token": token
        }, status=200)