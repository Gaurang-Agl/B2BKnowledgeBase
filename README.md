# TeamBoard — B2B Knowledge Base API

TeamBoard is a Django REST Framework backend API for a B2B Knowledge Base platform.

Companies can register and log in, receive a unique API key, search a curated knowledge base, and have their searches logged for usage tracking. Administrators can view overall API usage statistics.

## Features

* Company registration and login
* JWT-based authentication
* Automatic company creation using a Django `post_save` signal
* Unique API key generation
* Client and Admin company roles
* Protected Knowledge Base search API
* Search across both questions and answers
* Query logging for every valid Knowledge Base search
* Admin-only usage summary
* PostgreSQL database
* Dockerized PostgreSQL environment
* Environment-based database configuration
* Django ORM transactions for query logging
* REST API testing with Postman

## Technology Stack

* Python 3.14
* Django 6.1.1
* Django REST Framework 3.18.1
* Simple JWT 5.5.1
* PostgreSQL 17
* Docker & Docker Compose
* Python Dotenv
* Postman

## Project Structure

```text
B2BKnowledgeBase/
│
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── tests.py
│   └── views.py
│
├── teamboard/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── venv/
├── .env
├── .gitignore
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

## Data Models

### Company

Stores company information associated with a Django user.

Main fields:

* `user`
* `company_name`
* `api_key`
* `role`
* `created_at`

Roles:

* `admin`
* `client`

New companies default to the `client` role.

### KBEntry

Stores Knowledge Base content.

Fields:

* `question`
* `answer`
* `category`
* `created_at`

Supported categories:

* API
* Database
* Cloud
* Framework
* General

### QueryLog

Records every valid Knowledge Base search.

Fields:

* `company`
* `search_term`
* `results_count`
* `queried_at`

## Authentication

TeamBoard uses JSON Web Tokens (JWT) for API authentication.

Registration and login endpoints are public.

Knowledge Base and Admin Usage endpoints require a valid JWT access token.

The JWT access token should be sent using:

```text
Authorization: Bearer <access_token>
```

## API Endpoints

### 1. Register Company

```http
POST /api/auth/register/
```

Creates a new Django user and company.

The company is automatically created through a Django `post_save` signal, which also generates a unique API key.

#### Request

```json
{
    "username": "examplecompany",
    "email": "admin@example.com",
    "password": "ExamplePassword123!",
    "company_name": "Example Corporation"
}
```

#### Successful Response

**HTTP 201 Created**

```json
{
    "message": "Registration successful.",
    "username": "examplecompany",
    "company_name": "Example Corporation",
    "api_key": "<generated-api-key>",
    "access": "<jwt-access-token>"
}
```

The role is not accepted from the registration request and defaults to `client`.

---

### 2. Login

```http
POST /api/auth/login/
```

Authenticates an existing user and returns a fresh JWT access token.

#### Request

```json
{
    "username": "examplecompany",
    "password": "ExamplePassword123!"
}
```

#### Successful Response

**HTTP 200 OK**

```json
{
    "message": "Login successful.",
    "username": "examplecompany",
    "company_name": "Example Corporation",
    "api_key": "<api-key>",
    "access": "<jwt-access-token>"
}
```

Invalid credentials return:

**HTTP 401 Unauthorized**

---

### 3. Knowledge Base Query

```http
POST /api/kb/query/
```

Requires authentication.

Searches the Knowledge Base using the supplied search term.

The search is performed against both:

* `question`
* `answer`

#### Request

```json
{
    "search_term": "Django"
}
```

#### Successful Response

**HTTP 200 OK**

```json
{
    "search_term": "Django",
    "results_count": 2,
    "results": [
        {
            "id": 1,
            "question": "What is Django?",
            "answer": "Django is a Python web framework.",
            "category": "framework"
        }
    ]
}
```

A search with no matching results still returns:

**HTTP 200 OK**

```json
{
    "search_term": "xyznonexistent",
    "results_count": 0,
    "results": []
}
```

Every valid search is recorded in `QueryLog`, including searches that return zero results.

A missing or blank search term returns:

**HTTP 400 Bad Request**

---

### 4. Admin Usage Summary

```http
GET /api/admin/usag
```
