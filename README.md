# Speer Notes

![image](https://github.com/EGhost98/Speer_Notes/assets/76267623/cedacbda-942b-4c52-b530-ddc35e2b7c8b)

## How to Run the API Project
To run the project, follow these steps:

1. Clone the repository: `git clone <repository_url>`
2. Create a Virtual Python Environment `python -m venv env`.
3. Activate the Virtual Environment (if using Git-Bash) `source env/Scripts/Activate`
4. Navigate to the project directory: `cd Speer-Notes`
5. Install the dependencies: `pip install -r requirements.txt`
6. Change Database Parameters in .env as required. (local or Your Own Database or use the provided vercel Postgres Database).
7. Run the migrate command `python manage.py migrate`. (If Using your own Postgres Database)
8. Run the application: `python manage.py runserver`
9. Access the Swagger Open-API Documentation of API's at : `http://localhost:8000/swagger/`

## How to run the Tests

1. Follow Steps from above from 1-7.
2. Run `python manage.py test` (Using Django's Default Python standard unittest library).
3. Tests can be Found in test folder in each respective apps.

## Reason For Choice of Tech Stack

### Technologies Used

- **Programming Language:** Python
- **Backend Framework:** Django
- **REST Framework:** Django Rest Framework (DRF)
- **Database:** PostgreSQL
- **Test Framework:** Python Standard Unittest Library

### Why Python?

Python is a versatile and powerful programming language known for its readability, simplicity, and a vast ecosystem of libraries.

### Why Django?

Django is a high-level web framework for Python that encourages rapid development, clean and pragmatic design, and follows the "Don't Repeat Yourself" (DRY) principle. It provides a robust set of tools for building web applications, including an ORM for database interactions, a templating engine, and a built-in admin interface.

### Why Django Rest Framework (DRF)?

Django Rest Framework (DRF) is a powerful and flexible toolkit for building Web APIs in Django. It extends Django's capabilities to handle common patterns in API design, making it easy to build RESTful APIs. DRF provides features like serialization, authentication, and viewsets, simplifying the process of developing robust APIs.

### Why PostgreSQL?

PostgreSQL is a robust, open-source relational database management system. It is ACID compliant, supports complex queries, and has excellent performance. For efficient searching, we utilize indexing in PostgreSQL. Indexing enhances the speed of search operations by creating a data structure (index) on one or more columns, significantly reducing the time required to retrieve results.

### Why Python Standard Unittest Library?

Python's standard `unittest` library provides a simple and extensible testing framework. It allows for the creation of test cases and test suites, making it easy to write unit tests for Django applications. By using the standard `unittest` library, we ensure compatibility and maintainability of our test suite.

# API Documentation

## Authentication Endpoints

### 1. Sign Up

- **URL:** `/auth/signup/`
- **Method:** `POST`
- **Description:** Create a new user account.

### 2. Login

- **URL:** `/auth/login/`
- **Method:** `POST`
- **Description:** Log in to an existing user account and receive an access token.

### 3. Refresh Token

- **URL:** `/auth/refresh/`
- **Method:** `POST`
- **Description:** Refresh the access token.

### 4. Logout

- **URL:** `/auth/logout/`
- **Method:** `POST`
- **Description:** Log out and invalidate the refresh token.

## Note Endpoints

### 1. Get All Notes

- **URL:** `/api/notes/`
- **Method:** `GET`
- **Description:** Get a list of all notes for the authenticated user.

### 2. Get Note by ID

- **URL:** `/api/notes/:id/`
- **Method:** `GET`
- **Description:** Get a specific note by ID for the authenticated user.

### 3. Create New Note

- **URL:** `/api/notes/`
- **Method:** `POST`
- **Description:** Create a new note for the authenticated user.

### 4. Update Note by ID

- **URL:** `/api/notes/:id/`
- **Method:** `PUT`
- **Description:** Update an existing note by ID for the authenticated user.

### 5. Delete Note by ID

- **URL:** `/api/notes/:id/`
- **Method:** `DELETE`
- **Description:** Delete a note by ID for the authenticated user.

### 6. Share Note with Another User

- **URL:** `/api/notes/:id/share/`
- **Method:** `POST`
- **Description:** Share a note with another user using their email for the authenticated user.

### 7. Unshare Note with Another User

- **URL:** `/api/notes/:id/unshare/`
- **Method:** `POST`
- **Description:** Unshare a note with another user using their email for the authenticated user.

### 8. Make Note Public

- **URL:** `/api/notes/:id/make-public/`
- **Method:** `POST`
- **Description:** Make a note public for the authenticated user.

### 9. Make Note Private

- **URL:** `/api/notes/:id/make-private/`
- **Method:** `POST`
- **Description:** Make a note private(except for users in shared list) for the authenticated user.

### 10. Search Notes

- **URL:** `/api/search?q=:query`
- **Method:** `GET`
- **Description:** Search for notes based on keywords for the authenticated user.

## Swagger UI

- **URL:** `/swagger/`
- **Description:** Interactive API documentation using Swagger UI.
