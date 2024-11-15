from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey
from django.urls import reverse
from .models import Book
class BookAPITestCase(TestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='username1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(username='username2', email='user2@example.com', password='password')

        # Create API keys for both users, using the username as the API key name
        self.api_key_obj1, self.api_key1 = APIKey.objects.create_key(name=self.user1.username)
        self.api_key_obj2, self.api_key2 = APIKey.objects.create_key(name=self.user2.username)

        # Initialize the API client
        self.client = APIClient()

        # URLs
        self.book_list_url = reverse('book-list')    # URL pattern name for the BookViewSet list action
        self.book_detail_url = lambda pk: reverse('book-detail', args=[pk])  # URL pattern name for detail action

    ########### CREATE TEST #############

    def test_create_with_valid_payload_with_valid_api_key(self):
        """Create with valid payload and valid API key"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        payload = {
            "title": "Valid Book",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        response = self.client.post(self.book_list_url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().user, self.user1)

    def test_create_with_valid_payload_with_valid_api_key_but_without_published_date(self):
        """Create with valid payload and valid API key"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        payload = {
            "title": "Valid Book",
            "author": "Author One",
            "isbn": "1234567890123"
        }
        response = self.client.post(self.book_list_url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().user, self.user1)
    
    def test_create_with_valid_payload_with_valid_api_key_but_without_isbn(self):
        """Create with valid payload and valid API key"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        payload = {
            "title": "Valid Book",
            "author": "Author One",
            "isbn": "1234567890123"
        }
        response = self.client.post(self.book_list_url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().user, self.user1)
    
    def test_create_with_valid_payload_without_api_key(self):
        """Create with valid payload without API key"""
        self.client.credentials()  # Remove any credentials
        payload = {
            "title": "Book Without API Key",
            "author": "Author Two",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        response = self.client.post(self.book_list_url, payload, format='json')
        self.assertEqual(response.status_code, 401)  # Unauthorized due to lack of API key

    def test_create_with_invalid_payload_with_api_key(self):
        """Create with invalid payload (invalid ISBN, missing fields, wrong date format) with API key"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        payload = {
            # Missing 'title' and 'author'
            "published_date": "invalid-date-format",  # Invalid date format
            "isbn": "invalid-isbn"  # Invalid ISBN
        }
        response = self.client.post(self.book_list_url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        # Check if field are in response
        self.assertIn('title', response.data)
        self.assertIn('author', response.data)
        self.assertIn('published_date', response.data)
        self.assertIn('isbn', response.data)
    
    ########### GET TEST #############
        
    def test_create_and_get_with_valid_payload_with_api_key_from_user1(self):
        """Create and get with valid payload with API key from user 1"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        payload = {
            "title": "User1's Book",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        self.assertEqual(create_response.status_code, 201)
        book_id = create_response.data['id']

        # Get the book with user1's API key
        get_response = self.client.get(self.book_detail_url(book_id))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.data['title'], "User1's Book")

    def test_get_book_with_api_key_from_user2_should_return_404(self):
        """Try getting book previously created with API key 1, with API key 2"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        payload = {
            "title": "User1's Book",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Attempt to get the book with user2's API key
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key2)
        get_response = self.client.get(self.book_detail_url(book_id))
        self.assertEqual(get_response.status_code, 404)  # Should return 404 Not Found

    def test_get_list_with_api_key1_should_not_be_empty(self):
        """Get list with API key 1, should not be empty list"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book
        payload = {
            "title": "User1's Book",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        self.client.post(self.book_list_url, payload, format='json')
        # Get the list
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_get_list_with_api_key2_should_be_empty(self):
        """Get list with API key 2, should be empty list"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key2)
        # Get the list
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    ########### UPDATE TEST #############

    def test_update_with_valid_payload_with_api_key1(self):
        """Create with API key 1 and update valid with API key 1"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book
        payload = {
            "title": "Original Title",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Update the book
        update_payload = {
            "title": "Updated Title",
            "author": "Author One",
            "published_date": "2021-02-01",
            "isbn": "0987654321098"
        }
        update_response = self.client.put(self.book_detail_url(book_id), update_payload, format='json')
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['title'], "Updated Title")

    def test_update_with_valid_payload_with_api_key1_but_with_missing_isbn(self):
        """Create with API key 1 and update valid with API key 1"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book
        payload = {
            "title": "Original Title",
            "author": "Author One",
            "published_date": "2021-01-01",
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Update the book
        update_payload = {
            "title": "Updated Title",
            "author": "Author One",
            "published_date": "2021-02-01",
        }
        update_response = self.client.put(self.book_detail_url(book_id), update_payload, format='json')
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['title'], "Updated Title")
    

    def test_update_with_valid_payload_with_api_key1_but_add_missing_isbn(self):
        """Create with API key 1 and update valid with API key 1"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book
        payload = {
            "title": "Original Title",
            "author": "Author One",
            "published_date": "2021-01-01",
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Update the book
        update_payload = {
            "title": "Updated Title",
            "author": "Author One",
            "published_date": "2021-02-01",
            "isbn": "0987654321098"
        }
        update_response = self.client.put(self.book_detail_url(book_id), update_payload, format='json')
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['title'], "Updated Title")

    def test_update_with_invalid_isbn(self):
        """Update previously created book with invalid ISBN"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book
        payload = {
            "title": "Book to Update",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Update with invalid ISBN
        update_payload = {
            "title": "Book to Update",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "invalid-isbn"
        }
        update_response = self.client.put(self.book_detail_url(book_id), update_payload, format='json')
        self.assertEqual(update_response.status_code, 400)
        self.assertIn('isbn', update_response.data)

    def test_update_with_invalid_date_format(self):
        """Update previously created book with invalid date format"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book
        payload = {
            "title": "Book to Update",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Update with invalid date format
        update_payload = {
            "title": "Book to Update",
            "author": "Author One",
            "published_date": "invalid-date",
            "isbn": "1234567890123"
        }
        update_response = self.client.put(self.book_detail_url(book_id), update_payload, format='json')
        self.assertEqual(update_response.status_code, 400)
        self.assertIn('published_date', update_response.data)

    def test_update_with_empty_string_for_field(self):
        """Update previously created book with empty string for required field"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book
        payload = {
            "title": "Book to Update",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Update with empty 'title'
        update_payload = {
            "title": "",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        update_response = self.client.put(self.book_detail_url(book_id), update_payload, format='json')
        self.assertEqual(update_response.status_code, 400)
        self.assertIn('title', update_response.data)


    def test_update_with_valid_payload_but_with_api_key2(self):
        """Try updating previously created book with valid payload but with API key 2; should be denied"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book with user1
        payload = {
            "title": "User1's Book",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Attempt to update with user2's API key
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key2)
        update_payload = {
            "title": "Attempted Update",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        update_response = self.client.put(self.book_detail_url(book_id), update_payload, format='json')
        self.assertEqual(update_response.status_code, 404)  # Should be denied


    def test_delete_with_api_key1(self):
        """Create with API key 1 then delete with API key 1"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book
        payload = {
            "title": "Book to Delete",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Delete the book
        delete_response = self.client.delete(self.book_detail_url(book_id))
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_with_api_key2_should_be_denied(self):
        """Create with API key 1 then delete with API key 2; should be denied"""
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key1)
        # Create a book
        payload = {
            "title": "Book to Delete",
            "author": "Author One",
            "published_date": "2021-01-01",
            "isbn": "1234567890123"
        }
        create_response = self.client.post(self.book_list_url, payload, format='json')
        book_id = create_response.data['id']

        # Attempt to delete with user2's API key
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.api_key2)
        delete_response = self.client.delete(self.book_detail_url(book_id))
        self.assertEqual(delete_response.status_code, 404)  # Should be denied
        self.assertEqual(Book.objects.count(), 1)
