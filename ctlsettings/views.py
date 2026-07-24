import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def verify_turnstile_token(token, remote_ip=None):
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
    }
    if remote_ip:
        data["remoteip"] = remote_ip
    response = requests.post(url, data=data)
    result = response.json()
    return result.get("success", False)


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):

        print("Request data:", request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(
                {'error': 'Username and password must be provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Skip Turnstile in local development
        if settings.TURNSTILE_ENABLE and "localhost" not in request.META.get(
                "HTTP_ORIGIN"):
            token = request.data.get("turnstile_token")
            if not token:
                return Response(
                    {"error": "Missing Turnstile token"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            is_valid = verify_turnstile_token(
                token,
                request.META.get("REMOTE_ADDR")
            )
            if not is_valid:
                return Response(
                    {"error": "Invalid Turnstile token"},
                    status=status.HTTP_403_FORBIDDEN
                )
        # Continue with authentication logic here
        return Response({"success": True})
