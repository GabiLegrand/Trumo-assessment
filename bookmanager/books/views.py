from rest_framework.viewsets import ModelViewSet
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from .models import Book
from .serializers import BookSerializer
from django.contrib.auth.models import User

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [HasAPIKey]

    def _get_api_key(self):
        # Extract the API key from the request
        api_key_header = self.request.headers.get("Authorization")
        if api_key_header and api_key_header.startswith("Api-Key "):
            api_key = api_key_header.split("Api-Key ")[1]
            return api_key
        else:
            raise ValueError("API key is required for this operation.")

    def get_queryset(self):
        """
        Allow the user to only see it's own books
        """
        api_key = self._get_api_key()
        try:
            # Get the API key instance
            api_key_instance = APIKey.objects.get_from_key(api_key)
            # Assume the username is stored in the `name` of the API key
            user = User.objects.get(username=api_key_instance.name)
            # Filter books by the user
            return Book.objects.filter(user=user)
        except (APIKey.DoesNotExist, User.DoesNotExist):
            raise ValueError("Invalid API key or associated user does not exist.")
        
    def perform_create(self, serializer):
        api_key = self._get_api_key()
        try:
            # Get the API key instance
            api_key_instance = APIKey.objects.get_from_key(api_key)
            # Assume the username is stored in the `name` of the API key
            user = User.objects.get(username=api_key_instance.name)
            serializer.save(user=user)
        except (APIKey.DoesNotExist, User.DoesNotExist):
            raise ValueError("Invalid API key or associated user does not exist.")