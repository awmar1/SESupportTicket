# SE Support Tickets

A Django-based support ticket management system.

---

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv or venv (recommended)

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

the application will be available at: 

- Admin interface http://127.0.0.1:8000/admin/

---

### Project Structure

```
SESupportTickets/
├── logs/           # Log files
├── media/          # User-uploaded files
├── static/         # Static files
├── staticfiles/    # Collected static files
├── templates/      # HTML templates
└── SESupportTickets/
    ├── settings/   # Settings module
    │   ├── base.py
    │   ├── local.py
    │   └── production.py
    ├── urls.py
    └── wsgi.py
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

This README provides essential information for:

- Setting up the development environment
- Running the project locally
- Basic project structure
- Production deployment requirements
