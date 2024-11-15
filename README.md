# Description
**Note** : The base of the assignement was done in 3h20 mins, the dockerized version took me 4h40 due to troubleshooting the django/postgres integration

## Context  
This repository was created as part of an assessment during a recruitment process involving Gabriel LUDLE (Owner) and Trumo. The project was designed and completed within a 4-hour timeframe, as initially estimated by Gabriel before starting the task.

## Application  

This application is a multi-user API designed for book management. Users can register, update, retrieve, and delete their data using the API endpoints provided below. The application implements a simple API key-based authentication system, where each user is issued a unique API key upon account creation.  

### Note:  
The API key system is implemented as a basic proof-of-concept and requires further development to achieve full functionality and robustness.


# Implementation choices 

For this project, I chose Django as the backend framework. Django is my go-to framework when working with Python, thanks to its robustness and comprehensive feature set.  

### Implementation Details  

- **Django REST Framework and ModelViewSet**  
  Since the API was centered around a single table, `Book`, I utilized Django REST Framework's `ModelViewSet`. This allowed me to efficiently generate CRUD routes with minimal code—just five lines—while maintaining scalability and clean architecture.  

- **Extending the Assignment Scope**  
  While the assignment only required operations on the `Book` table, I felt the project would be too simplistic without additional features. To enhance the project, I implemented a basic authentication system, including unit tests to ensure its reliability.

- **Authentication System**  
  I opted for an API key-based authentication system since the project is purely backend and API-focused. This approach ensures ease of use and aligns well with the project requirements. However, I could have also implemented OAuth or JWT token authentication for more advanced use cases or future expansion.  



# Installation
## Running the Project Locally  
**/!\ for the easy setup, i have left the `.env` file in the repo, but i would not have done the same for a production grade repo**\
To run this project on your local machine, follow these steps:

### Steps to Set Up with docker 
1. Clone the repository to your local environment.  
2. Navigate to the root folder and execute the following commands:  
```shell
docker-compose up --build
```
be sure to have docker installed on your machine

### Steps to Set Up local instance (Without docker)
1. Clone the repository to your local environment.  
2. In the `.env` file, located in `./bookmanager/.env`, change the value of `USE_LOCAL` by 
```shell
USE_LOCAL=True
```
3. Navigate to the root folder and execute the following commands:  

```bash
# Install the required dependencies
pip install -r requirements.txt

# Navigate to the application directory
cd ./bookmanager

# Generate and apply database migrations
python ./manage.py makemigrations
python ./manage.py migrate

# Run the local server on port 5000 (or replace with your desired port)
python ./manage.py runserver 5000
```

### Tips for Production Deployment 

1. If you plan to deploy this Django project using **Passenger WSGI**, configure the `application` in the `wsgi.py` file as follows:  

```python
import engine.wsgi
application = engine.wsgi.application
```

This configuration ensures the application integrates smoothly with the Passenger WSGI server for production use. 

2. In the `.env` file, located in `./bookmanager/.env`, change the value of `DEBUG` by 
```shell
DEBUG=False
```

## Runing unit test

The API utilizes Django's native testing framework, ensuring a robust and systematic testing process. Below are the commands for running tests:

### Running All Tests
To execute all tests within the application, use the following commands:
```bash
cd ./bookmanager  # If not already in the directory
python manage.py test
```

### Testing Only the Book API
To test functionalities specific to the Book API, run:
```bash
cd ./bookmanager  # If not already in the directory
python manage.py test books.tests
```

### Testing Only the User Registration API
For testing features related to user registration and authentication, use:
```bash
cd ./bookmanager  # If not already in the directory
python manage.py test api_auth.tests
```

These commands allow for targeted and comprehensive testing of the application's individual components.

---


# API Documentation
Practical usage example is available in the file `tests/usage_example.py`

### **User Registration API**

**Endpoint**: `/api/register/`

**Description**: This endpoint creates a new user and automatically generates an API key associated with the user.

#### Request

- **Method**: `POST`
- **Content-Type**: `application/json`
- **Payload**:

```json
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123"
}
```

#### Response

- **Success Response (201 Created)**:

```json
{
    "username": "testuser",
    "email": "testuser@example.com",
    "api_key": "12345abcdef67890"
}
```

- **Error Responses**:
  - **400 Bad Request**: If required fields are missing or invalid.
  - **409 Conflict**: If the username or email is already taken.

---

### **Books API**

#### **Base URL**: `/books/`

This API allows authenticated users to manage their books. API key authentication is required for all endpoints.

---

### **1. Create a Book**

**Endpoint**: `/books/`

**Description**: Create a new book linked to the authenticated user.

#### Request

- **Method**: `POST`
- **Content-Type**: `application/json`
- **Headers**:

```text
Authorization: Api-Key <your_api_key>
```

- **Payload**:

```json
{
    "title": "Book Title",
    "author": "Author Name",
    "published_date": "2021-01-01",
    "isbn": "1234567890123"
}
```

#### Response

- **Success Response (201 Created)**:

```json
{
    "id": 1,
    "title": "Book Title",
    "author": "Author Name",
    "published_date": "2021-01-01",
    "isbn": "1234567890123",
    "creation_date": "2024-11-15T12:00:00Z",
    "user": 1
}
```

- **Error Responses**:
  - **400 Bad Request**: Invalid data, e.g., missing required fields or incorrect ISBN format.
  - **403 Forbidden**: Missing or invalid API key.

---

### **2. Get List of Books**

**Endpoint**: `/books/`

**Description**: Retrieve all books linked to the authenticated user.

#### Request

- **Method**: `GET`
- **Headers**:

```text
Authorization: Api-Key <your_api_key>
```

#### Response

- **Success Response (200 OK)**:

```json
[
    {
        "id": 1,
        "title": "Book Title",
        "author": "Author Name",
        "published_date": "2021-01-01",
        "isbn": "1234567890123",
        "creation_date": "2024-11-15T12:00:00Z",
        "user": 1
    }
]
```

- **Error Responses**:
  - **403 Forbidden**: Missing or invalid API key.
  - **200 OK with Empty List**: No books found for the user.

---

### **3. Get a Specific Book**

**Endpoint**: `/books/{id}/`

**Description**: Retrieve details of a specific book linked to the authenticated user.

#### Request

- **Method**: `GET`
- **Headers**:

```text
Authorization: Api-Key <your_api_key>
```

#### Response

- **Success Response (200 OK)**:

```json
{
    "id": 1,
    "title": "Book Title",
    "author": "Author Name",
    "published_date": "2021-01-01",
    "isbn": "1234567890123",
    "creation_date": "2024-11-15T12:00:00Z",
    "user": 1
}
```

- **Error Responses**:
  - **403 Forbidden**: Missing or invalid API key.
  - **404 Not Found**: The book does not exist or does not belong to the authenticated user.

---

### **4. Update a Book**

**Endpoint**: `/books/{id}/`

**Description**: Update an existing book linked to the authenticated user.

#### Request

- **Method**: `PUT`
- **Headers**:

```text
Authorization: Api-Key <your_api_key>
```

- **Payload**:

```json
{
    "title": "Updated Title",
    "author": "Updated Author",
    "published_date": "2022-01-01",
    "isbn": "0987654321098"
}
```

#### Response

- **Success Response (200 OK)**:

```json
{
    "id": 1,
    "title": "Updated Title",
    "author": "Updated Author",
    "published_date": "2022-01-01",
    "isbn": "0987654321098",
    "creation_date": "2024-11-15T12:00:00Z",
    "user": 1
}
```

- **Error Responses**:
  - **400 Bad Request**: Invalid data.
  - **403 Forbidden**: Missing or invalid API key.
  - **404 Not Found**: The book does not exist or does not belong to the authenticated user.

---

### **5. Delete a Book**

**Endpoint**: `/books/{id}/`

**Description**: Delete a specific book linked to the authenticated user.

#### Request

- **Method**: `DELETE`
- **Headers**:

```text
Authorization: Api-Key <your_api_key>
```

#### Response

- **Success Response (204 No Content)**:

```text
(no content)
```

- **Error Responses**:
  - **403 Forbidden**: Missing or invalid API key.
  - **404 Not Found**: The book does not exist or does not belong to the authenticated user.

---
# Detail about the unit test
This section provides an overview of the unit tests included in the project. Please note that this information is included solely for the purpose of the assignment and would not typically be part of a production-grade project.

## Books api unit test
**Setup Method**: Creates two users and generates API keys for them. Initializes the API client and defines URLs for list and detail actions.

### Create Tests:

**Valid Payload with Valid API Key**: Ensures that a book can be created when a valid API key and valid data are provided. \
**Valid Payload with Valid API Key and missing fields**: Ensures that a book can be created when a valid API key and valid data are provided and non mandatory field are missing. \
**Valid Payload without API Key**: Checks that creation is denied when no API key is provided. \
**Invalid Payload with API Key**: Verifies that appropriate errors are returned when invalid data is submitted.

### Get Tests:

**Get with Correct API Key**: Confirms that a user can retrieve their own book. \
**Get with Different User's API Key**: Ensures that a user cannot access another user's book (should return 404). \
**Get List with API Key 1**: The list should contain the book created by user 1. \
**Get List with API Key 2**: The list should be empty for user 2 since they haven't created any books.

### Update Tests:

**Valid Update with Correct API Key**: Checks that a user can update their own book. \
**Valid Update with Correct API Key but missing isbn**: Checks if the datavalidation of the isbn doesn't produce error \
**Valid Update with Correct API Key but add missing isbn**: Checks if adding a missing field  \
**Update with Invalid ISBN**: Validates that updating with an invalid ISBN is rejected. \
**Update with Invalid Date Format**: Ensures that an invalid date format is not accepted. \
**Update with Empty String for Field**: Verifies that required fields cannot be empty. \
**Update with Valid Payload but Wrong API Key**: Confirms that a user cannot update another user's book.

### Delete Tests:

**Delete with Correct API Key**: Checks that a user can delete their own book. \
**Delete with Different User's API Key**: Ensures that a user cannot delete another user's book.
