from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_api_key.models import APIKey

class CreateUserAPIView(APIView):
    """
    For simplicity, this route allow the creation of an user and create automatically an api key
    This route is only for the assessment and simplify the authentification process to have an 
    multi user api
    """
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks

    def post(self, request, *args, **kwargs):
        # Extract user information from the payload
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate payload
        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Generate an API key for the user
        api_key, key = APIKey.objects.create_key(name=username)

        # Return user details and the API key
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "api_key": key,
            },
            status=status.HTTP_201_CREATED,
        )