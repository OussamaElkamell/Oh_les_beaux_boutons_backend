# NIRD swipe - Django Backend

This is the Django REST Framework backend for NIRD swipe.

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd django
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your settings.

### 4. Create and Run Migrations

**IMPORTANT:** You must create migrations first before running migrate:

```bash
# Create migrations for all apps
python manage.py makemigrations users cards results

# Apply migrations to database
python manage.py migrate
```

### 5. Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Cards

- `GET /api/cards/` - List all technology cards
- `GET /api/cards/random/?count=15` - Get random selection of cards
- `GET /api/cards/{id}/` - Get specific card

### Results

- `POST /api/results/` - Save game results
- `GET /api/results/` - Get user's game history

### Authentication

- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/register/` - Register new user

## Admin Panel

Access the admin panel at `http://localhost:8000/admin/`

## Connecting to Frontend

Update your frontend to use the API endpoints. The CORS is configured to allow requests from `localhost:5173` (Vite default) and `localhost:3000`.

For production, update `CORS_ALLOWED_ORIGINS` in `settings.py`.
