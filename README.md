# Task Management REST API

A RESTful API for managing tasks, built with Python, Flask, SQLite, and SQLAlchemy ORM. Features session-based authentication and user-specific task management.

## Features

- User registration and authentication
- Session-based login/logout
- Full CRUD operations for tasks
- User-specific task isolation (users can only access their own tasks)
- Input validation and error handling
- RESTful API design with proper HTTP status codes

## Tech Stack

- **Python 3.x** - Programming language
- **Flask** - Web framework
- **SQLite** - Database
- **SQLAlchemy** - ORM (Object-Relational Mapping)
- **Flask-CORS** - Cross-Origin Resource Sharing support

## Project Structure
```
task-management-api/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── config.py             # Configuration settings
│   ├── models.py             # User & Task models
│   └── routes/
│       ├── __init__.py
│       ├── auth.py           # Authentication endpoints
│       ├── helpers.py        # Auth helper functions
│       └── tasks.py          # Task CRUD endpoints
├── instance/
│   └── tasks.db              # SQLite database
├── docs/
│   └── postman_collection.json
├── venv/                     # Virtual environment
├── .gitignore
├── requirements.txt
├── run.py                    # Entry point
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/task-management-api.git
cd task-management-api
```

2. Create virtual environment
```bash
python3 -m venv venv
```

3. Activate virtual environment
```bash
source venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Run the application
```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login user |
| POST | /api/auth/logout | Logout user |
| GET | /api/auth/me | Get current user |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/tasks | Get all tasks (for logged-in user) |
| POST | /api/tasks | Create new task |
| GET | /api/tasks/:id | Get task by ID |
| PUT | /api/tasks/:id | Update task |
| DELETE | /api/tasks/:id | Delete task |

## Request & Response Examples

### Register User

**Request:**
```http
POST /api/auth/register
Content-Type: application/json

{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "secretpassword"
}
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "created_at": "2025-01-09T10:30:00"
    }
}
```

### Login

**Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "secretpassword"
}
```

**Response (200 OK):**
```json
{
    "message": "Logged in successfully",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "created_at": "2025-01-09T10:30:00"
    }
}
```

### Create Task

**Request:**
```http
POST /api/tasks
Content-Type: application/json

{
    "title": "Complete project",
    "description": "Finish the REST API project",
    "priority": "high"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "title": "Complete project",
    "description": "Finish the REST API project",
    "status": "pending",
    "priority": "high",
    "due_date": null,
    "created_at": "2025-01-09T10:35:00",
    "updated_at": "2025-01-09T10:35:00",
    "user_id": 1
}
```

### Get All Tasks

**Request:**
```http
GET /api/tasks
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "title": "Complete project",
        "description": "Finish the REST API project",
        "status": "pending",
        "priority": "high",
        "due_date": null,
        "created_at": "2025-01-09T10:35:00",
        "updated_at": "2025-01-09T10:35:00",
        "user_id": 1
    }
]
```

### Update Task

**Request:**
```http
PUT /api/tasks/1
Content-Type: application/json

{
    "status": "in_progress",
    "priority": "medium"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Complete project",
    "description": "Finish the REST API project",
    "status": "in_progress",
    "priority": "medium",
    "due_date": null,
    "created_at": "2025-01-09T10:35:00",
    "updated_at": "2025-01-09T10:40:00",
    "user_id": 1
}
```

### Delete Task

**Request:**
```http
DELETE /api/tasks/1
```

**Response (200 OK):**
```json
{
    "message": "Task 1 deleted successfully"
}
```

## Validation Rules

### Task Fields

| Field | Type | Required | Allowed Values |
|-------|------|----------|----------------|
| title | string | Yes | Any text (max 100 chars) |
| description | string | No | Any text |
| status | string | No | pending, in_progress, completed |
| priority | string | No | low, medium, high |
| due_date | datetime | No | ISO 8601 format |

### User Fields

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| username | string | Yes | Unique, max 80 chars |
| email | string | Yes | Unique, valid email format |
| password | string | Yes | Min 1 char |

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid data provided |
| 401 | Unauthorized - Login required |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 405 | Method Not Allowed - Invalid HTTP method |
| 409 | Conflict - Resource already exists |
| 500 | Internal Server Error - Server error |

## Testing with Postman

A Postman collection is included in the `docs/` folder. To use it:

1. Open Postman
2. Click "Import"
3. Select `docs/postman_collection.json`
4. All endpoints will be available in the collection
