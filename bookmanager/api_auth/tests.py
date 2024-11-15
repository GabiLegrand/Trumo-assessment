from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey

class CreateUserAPITestCase(TestCase):

    def setUp(self):
        # Setup initial data if needed
        self.register_url = reverse('user-register')  # Ensure the name matches your urls.py
        self.valid_payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
        self.invalid_payload = {
            "username": "",  # Invalid: Missing username
            "email": "invalid@example.com",
            "password": "securepassword123"
        }

    def test_create_user_success(self):
        """Test creating a user with valid data returns the expected response."""
        response = self.client.post(self.register_url, self.valid_payload, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("api_key", response.data)  # Check if API key is in the response
        self.assertEqual(response.data["username"], self.valid_payload["username"])
        self.assertEqual(response.data["email"], self.valid_payload["email"])

        # Check if the user was created
        user_exists = User.objects.filter(username=self.valid_payload["username"]).exists()
        self.assertTrue(user_exists)

        # Check if the API key was created
        api_key_exists = APIKey.objects.filter(name=self.valid_payload["username"]).exists()
        self.assertTrue(api_key_exists)

    def test_create_user_with_existing_username(self):
        """Test creating a user with an existing username fails."""
        # Create a user manually
        User.objects.create_user(**self.valid_payload)

        response = self.client.post(self.register_url, self.valid_payload, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Username already exists.")

    def test_create_user_invalid_payload(self):
        """Test creating a user with invalid data returns an error."""
        response = self.client.post(self.register_url, self.invalid_payload, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Username and password are required.")

    def test_create_user_with_missing_field(self):
        """Test creating a user with a missing field in the payload."""
        incomplete_payload = {
            "username": "incompleteuser",
            "password": "securepassword123"  # Missing email
        }

        response = self.client.post(self.register_url, incomplete_payload, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], incomplete_payload["username"])
        self.assertEqual(response.data["email"],'')  # Email should be None or blank
