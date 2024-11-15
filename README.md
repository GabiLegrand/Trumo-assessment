# API Documentation

---

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

# UNIT TEST

## Books api unit test
**Setup Method**: Creates two users and generates API keys for them. Initializes the API client and defines URLs for list and detail actions.

### Create Tests:

**Valid Payload with Valid API Key**: Ensures that a book can be created when a valid API key and valid data are provided.
**Valid Payload with Valid API Key and missing fields**: Ensures that a book can be created when a valid API key and valid data are provided and non mandatory field are missing.
**Valid Payload without API Key**: Checks that creation is denied when no API key is provided.
**Invalid Payload with API Key**: Verifies that appropriate errors are returned when invalid data is submitted.

### Get Tests:

**Get with Correct API Key**: Confirms that a user can retrieve their own book.
**Get with Different User's API Key**: Ensures that a user cannot access another user's book (should return 404).
**Get List with API Key 1**: The list should contain the book created by user 1.
**Get List with API Key 2**: The list should be empty for user 2 since they haven't created any books.

### Update Tests:

**Valid Update with Correct API Key**: Checks that a user can update their own book.
**Valid Update with Correct API Key but missing isbn**: Checks if the datavalidation of the isbn doesn't produce error
**Valid Update with Correct API Key but add missing isbn**: Checks if adding a missing field 
**Update with Invalid ISBN**: Validates that updating with an invalid ISBN is rejected.
**Update with Invalid Date Format**: Ensures that an invalid date format is not accepted.
**Update with Empty String for Field**: Verifies that required fields cannot be empty.
**Update with Valid Payload but Wrong API Key**: Confirms that a user cannot update another user's book.

### Delete Tests:

**Delete with Correct API Key**: Checks that a user can delete their own book.
**Delete with Different User's API Key**: Ensures that a user cannot delete another user's book.
