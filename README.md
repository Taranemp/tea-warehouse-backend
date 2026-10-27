# Tea Warehouse Backend

A Django REST Framework backend for a **tea factory warehouse management system**. It exposes the REST API used by the [frontend](https://github.com/Taranemp/tea-warehouse-frontend).

## Features

- Token-based authentication (register, login, current user)
- Factory management API (create, list, update, delete)
- Core data and product management endpoints
- Seed command that creates a ready-to-use admin account
- Django admin panel for managing data

## Tech Stack

- Python 3
- Django
- Django REST Framework
- SQLite (development database)

## Getting Started

### Prerequisites

- Python 3.10 or newer
- pip

### 1. Clone the repository

```bash
git clone https://github.com/Taranemp/tea-warehouse-backend.git
cd tea-warehouse-backend
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows (Git Bash)
source .venv/Scripts/activate

# Windows (CMD / PowerShell)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root based on `.env.sample`:

```bash
cp .env.sample .env
```

Then open `.env` and fill in your values (for example `SECRET_KEY` and `DEBUG`).

> Never commit your real `.env` file.

### 4. Set up the database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed initial data

```bash
python manage.py seed_data
```

This creates a development superuser:

| Field    | Value           |
| -------- | --------------- |
| Username | `admin`         |
| Password | `admin`         |
| Email    | `admin@admin.com` |

> **Warning:** these credentials are for local development only. Change them (or remove the seed user) before deploying anywhere public.

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin/`.

## Connecting the Frontend

In the frontend project, set the API base URL in your `.env.development` file to point to this server, for example:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

If the browser blocks requests with a CORS error, make sure the frontend origin (for example `http://localhost:5173`) is allowed in the backend CORS settings.

## Project Structure

```
tea-warehouse-backend/
├── manage.py
├── requirements.txt
├── .env.sample
└── ...            # Django project and app folders
```

## Useful Commands

| Command                              | Description                  |
| ------------------------------------ | ---------------------------- |
| `python manage.py runserver`         | Start the development server |
| `python manage.py createsuperuser`   | Create an admin user manually |
| `python manage.py seed_data`         | Create the seed admin account |
| `python manage.py test`              | Run the test suite           |

## Roadmap

- [ ] Inventory and stock movement endpoints
- [ ] Role-based permissions
- [ ] API documentation (Swagger / OpenAPI)
- [ ] PostgreSQL support for production

## Author

**Taranemp**: [GitHub](https://github.com/Taranemp)

## License

This project is currently unlicensed. All rights reserved.