import requests

BASE_URL = "http://127.0.0.1:5000/books/"  # Update this with your actual API URL

def make_request(payload):

    response = requests.post(BASE_URL, json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_create_book():
    print("## Testing book creation isbn 10...")
    payload = {
        "title": "Test book",
        "author": "Gabriel ludel",
        "published_date": "1998-07-14",
        "isbn": "1234567890",
    }
    make_request(payload)
    print("## Testing book creation isbn 13...")
    payload = {
        "title": "Test book",
        "author": "Gabriel ludel",
        "published_date": "1998-07-14",
        "isbn": "1234567890123",
    }
    make_request(payload)

def test_create_book_wrong():
    print("## Testing book creation wrong isbn...")
    payload = {
        "title": "Test book",
        "author": "Gabriel ludel",
        "published_date": "1998-07-14",
        "isbn": "1234",
    }
    make_request(payload)
    
    print("## Testing book creation no publish date...")
    payload = {
        "title": "Test book",
        "author": "Gabriel ludel",
        "isbn": "1234567890123",
    }
    make_request(payload)
    
    print("## Testing book creation No title...")
    payload = {
        "author": "Gabriel ludel",
        "published_date": "1998-07-14",
        "isbn": "1234567890123",
    }
    make_request(payload)
    
    print("## Testing book creation no author...")
    payload = {
        "title": "Test book",
        "author": "Gabriel ludel",
        "published_date": "1998-07-14",
        "isbn": "1234567890123",
    }
    make_request(payload)

    print("## Testing book creation multiple field missing...")
    payload = {
        "published_date": "1998-07-14",
        "isbn": "1234567890123",
    }
    make_request(payload)



def test_list_books():
    print("\nTesting listing books...")
    response = requests.get(BASE_URL)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_get_book(book_id):
    print(f"\nTesting retrieving book with ID {book_id}...")
    response = requests.get(f"{BASE_URL}{book_id}/")
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_update_book(book_id):
    print(f"\nTesting updating book with ID {book_id}...")
    payload = {
        "title": "Updated Django for APIs",
        "author": "William S. Vincent",
        "published_date": "2022-03-01",
        "isbn": "1234567890123",
    }
    response = requests.put(f"{BASE_URL}{book_id}/", json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_partial_update_book(book_id):
    print(f"\nTesting partial update for book with ID {book_id}...")
    payload = {
        "title": "Partially Updated Django for APIs"
    }
    response = requests.patch(f"{BASE_URL}{book_id}/", json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_delete_book(book_id):
    print(f"\nTesting deleting book with ID {book_id}...")
    response = requests.delete(f"{BASE_URL}{book_id}/")
    print("Status Code:", response.status_code)
    if response.status_code == 204:
        print("Book deleted successfully.")
    else:
        print("Response:", response.json())

if __name__ == "__main__":
    # Create a new book
    print('** creation')
    test_create_book()
    print('** creation failtest')
    test_create_book_wrong()


    # # List all books
    # test_list_books()

    # # Retrieve a specific book (Update the ID after testing create)
    # test_get_book(1)

    # # Update a specific book
    # test_update_book(1)

    # # Partially update a specific book
    # test_partial_update_book(1)

    # # Delete a specific book
    # test_delete_book(1)

    # # Verify the book is deleted by listing all books again
    # test_list_books()