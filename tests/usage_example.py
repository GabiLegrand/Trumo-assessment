import requests
import random
BASE_URL = "http://127.0.0.1:5000/"  # Update this with your actual API URL

### Python Examples for api usage 

# **Register a New User**
rand_number = random.randint(0,1000) # Add random number to allow multiple usage of this test script
url =  BASE_URL + "api/register/"
payload = {
    "username": f"testuser_{rand_number}" , # Mandatory
    "email": "testuser@example.com", # Mandatory
    "password": "password123" # Mandatory
}
response = requests.post(url, json=payload)
print(response.json())
if response.status_code < 300:
    user_data = response.json()
    api_key = user_data['api_key']
    print("Successful creation of a new user, status code :", response.status_code)
else :
    raise Exception('Error, the creation of the new user failed')

########
url = BASE_URL + "books/"
# Add the api-key header to all request otherwise, the api will answer "unauthorized"
headers = {
    "Authorization": f"Api-Key {api_key}"
}
# Create a Book

payload = {
    "title": "Book Title", # Mandatory
    "author": "Author Name", # Mandatory
    "published_date": "2021-01-01", # Optional, YYYY-MM-DD format only
    "isbn": "1234567890123" # Optional, 10 or 13 digit only
}
response = requests.post(url, headers=headers, json=payload)
if response.status_code < 300:
    book_data = response.json()
    book_id = book_data['id']
    print("Successful creation of a new book, status code :", response.status_code)
else :
    raise Exception('Error, the creation of the new book failed')

# Get List of Books

response = requests.get(url, headers=headers)
if response.status_code < 300:
    print("Successfully fetched all books, status code :",  response.status_code)
else :
    raise Exception('Error, the fetching of the books failed')

# Get Only one Book

response = requests.get(url + f'{book_id}/', headers=headers)
if response.status_code < 300:
    print("Successfully fetched one specific book, status code :",  response.status_code)
else :
    raise Exception('Error, the fetching of the book failed')

# Update a Book

payload = {
    "title": "Updated Title",
    "author": "Updated Author",
    "published_date": "2022-01-01",
    "isbn": "0987654321098"
}
response = requests.put(url + f'{book_id}/', headers=headers, json=payload)
if response.status_code < 300:
    print("Successfully updated the book, status code :",  response.status_code)
else :
    raise Exception('Error, the update of the book failed')

# Delete a Book

response = requests.delete(url+ f'{book_id}/', headers=headers)
if response.status_code < 300:
    print("Successfully deleted the book, status code :",  response.status_code)
else :
    raise Exception('Error, the deletion of the book failed')
