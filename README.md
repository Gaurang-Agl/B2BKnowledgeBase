# TeamBoard — B2B Knowledge Base API

## Overview

TeamBoard is a Django REST API platform for B2B companies to query a centralized Knowledge Base using secure JWT authentication.

The system supports:

- Company registration
- Automatic API key generation
- JWT authentication
- Knowledge Base search
- Query logging
- Admin usage statistics
- PostgreSQL database
- Docker-based PostgreSQL setup
- Seed data for the Knowledge Base

## Tech Stack

- Python 3.14
- Django 6.1
- Django REST Framework
- Simple JWT
- PostgreSQL 17
- Docker / Docker Compose
- Postman

## Project Structure

B2BKnowledgeBase/
├── api/
│   ├── management/
│   │   └── commands/
│   │       └── seed_kb.py
│   ├── migrations/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── tests.py
│   └── views.py
├── teamboard/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── B2BKnowledgeBase_Postman_Collection.json

## Prerequisites

- Python 3.14+
- Docker Desktop
- Git
- Postman

## Setup

Clone the repository:

git clone https://github.com/Gaurang-Agl/B2BKnowledgeBase.git

cd B2BKnowledgeBase

Create and activate the virtual environment:

python -m venv venv

PowerShell:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

## Environment Configuration

Create a `.env` file in the project root.

Example:

DJANGO_SECRET_KEY='your-secret-key'
POSTGRES_DB=teamboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD='your-password'
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

Do not commit `.env` to Git.

## PostgreSQL with Docker

Start PostgreSQL:

docker compose up -d

Check the container:

docker compose ps

The PostgreSQL service runs on port 5432.

## Database Migration

Run:

python manage.py makemigrations
python manage.py migrate

## Seed Knowledge Base

Populate the Knowledge Base:

python manage.py seed_kb

Verify the number of entries:

python manage.py shell -c "from api.models import KBEntry; print('KB entries:', KBEntry.objects.count())"

The project contains at least 10 Knowledge Base entries.

## Run the API

python manage.py runserver

The API is available at:

http://127.0.0.1:8000/

## API Endpoints

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| POST | /api/auth/register/ | Public | Register a company |
| POST | /api/auth/login/ | Public | Login and receive JWT |
| POST | /api/kb/query/ | JWT | Search the Knowledge Base |
| GET | /api/admin/usage-summary/ | Admin JWT | View usage statistics |

## Authentication

Protected endpoints require:

Authorization: Bearer <access_token>

The JWT access token is returned during registration and login.

## Register

POST /api/auth/register/

Request:

{
    "username": "acmecorp",
    "password": "securepass123",
    "company_name": "Acme Corp",
    "email": "dev@acmecorp.com"
}

A successful registration returns:

- username
- company_name
- automatically generated api_key
- JWT access token

The API key is generated server-side.

## Login

POST /api/auth/login/

Request:

{
    "username": "acmecorp",
    "password": "securepass123"
}

## Knowledge Base Query

POST /api/kb/query/

Header:

Authorization: Bearer <access_token>

Request:

{
    "search": "Django"
}

Response:

{
    "search": "Django",
    "count": 3,
    "results": [
        {
            "id": 1,
            "question": "What is Django?",
            "answer": "...",
            "category": "framework"
        }
    ]
}

The search checks both Knowledge Base questions and answers.

Every query is recorded in `QueryLog`.

## No Matching Results

Request:

{
    "search": "xyznonexistent999"
}

Response:

{
    "search": "xyznonexistent999",
    "count": 0,
    "results": []
}

A query with no matches is still logged.

## Admin Usage Summary

GET /api/admin/usage-summary/

Requires a JWT belonging to a company whose role is `admin`.

Response:

{
    "total_queries": 2,
    "active_companies": 1,
    "top_search_terms": [
        {
            "search_term": "Django",
            "count": 1
        }
    ]
}

`active_companies` represents companies that have generated QueryLog records.

## Making a Company an Admin

For local testing:

python manage.py shell

Then:

from django.contrib.auth.models import User
from api.models import Company

user = User.objects.get(username="postmanclient")
user.company.role = Company.Role.ADMIN
user.company.save()

Exit the shell with:

exit()

## Testing

Run Django system checks:

python manage.py check

Run automated tests:

python manage.py test

The project includes tests covering authentication, Knowledge Base queries, permissions, and usage statistics.

## Postman

The repository contains:

B2BKnowledgeBase_Postman_Collection.json

The collection covers the required API scenarios:

1. Register a new company
2. Register with duplicate username
3. Login with valid credentials
4. Login with wrong password
5. Query KB without token
6. Query KB with valid token and matching results
7. Query KB with valid token and no matching results
8. Query KB with missing search field
9. Usage summary with CLIENT token
10. Usage summary with ADMIN token
11. Verify QueryLog records in PostgreSQL/PGAdmin

Import the collection into Postman and start the Django server before executing the API requests.

## QueryLog Verification

After executing Knowledge Base queries, QueryLog records can be verified using PGAdmin or Django shell.

Example:

python manage.py shell -c "from api.models import QueryLog; print(list(QueryLog.objects.values('search_term','results_count','company_id','queried_at')))"

The query log contains:

- company
- search term
- number of results
- query timestamp

## License

This project was created as a backend API assignment/project.