# SE Support Tickets

A Django REST API for managing support tickets with agent assignment and status tracking capabilities.

---

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv or venv (recommended)

## Features

- Automatic ticket assignment to agents
- Status transition management
- Swagger/OpenAPI documentation
- Concurrent-safe operations
- REST API endpoints

## Tech Stack

- Python 3.x
- Django REST Framework
- drf-yasg (Swagger/OpenAPI)
- PostgreSQL

---

## API Endpoints

### Tickets

- `GET /api/tickets/ticket/` - List all tickets
- `POST /api/tickets/ticket/` - Create a new ticket
- `GET /api/tickets/ticket/{id}/` - Get ticket details
- `PUT /api/tickets/ticket/{id}/` - Update ticket
- `DELETE /api/tickets/ticket/{id}/` - Delete ticket

### Assignment
- `POST /api/tickets/ticket/assign/` - Assign batch of tickets to agent
  ```json
  {
    "batch_size": 10
  }
  ```

### Agent Actions
- `GET /api/tickets/ticket/my_tickets/ ` - List tickets assigned to the authenticated agent

- `POST /api/tickets/ticket/{id}/status/` - Update ticket status
  ```json
  {
    "status": "in_progress"
  }
  ```

### Authentication
- `POST /api/token/` -Obtain JWT token pair
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
  
- `POST /api/token/refresh/` - Refresh access token

```json
{
  "refresh": "your_refresh_token"
}
```

## API Documentation

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`
- OpenAPI JSON: `/swagger.json`


---

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd SESupportTickets
```

2. Create a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

---

## Run the development server:

1.Ensure you're using local settings:
```
# Windows
set DJANGO_SETTINGS_MODULE=SESupportTickets.settings.local
# Linux/MacOS
export DJANGO_SETTINGS_MODULE=SESupportTickets.settings.local
```

2. Start the server:
```bash
python manage.py runserver
```


---

## Production Setup

For production, you should set up a web server (like Nginx or Apache) and a WSGI server (like Gunicorn or uWSGI).

set these environment variables:

```
DJANGO_SETTINGS_MODULE=SESupportTickets.settings.production
DJANGO_SECRET_KEY=<your-secret-key>
DB_NAME=<db-name>
DB_USER=<db-user>
DB_PASSWORD=<db-password>
DB_HOST=<db-host>
DB_PORT=5432
```

then run:

```bash
python manage.py collectstatic
python manage.py migrate
```
---

## Testing

### Running Tests

Run all tests:

```bash
python manage.py test
```

Load Test Data (Creates 1000 test tickets):

```bash
python manage.py populate_tickets 1000
```

---

The README includes:
- Overview of functionality
- API endpoints
- Status workflow diagram
- Setup instructions
- Authentication details
- Documentation links