# Expense Tracker API 💸

A backend solution for personal finance management, built with Django REST Framework (DRF). This API enables users to track expenses, generate analytical reports, and manage categories with secure, permission-based access.

## 🚀 Key Features

- **User Isolation**: Data is segmented per user; you only see the expenses you created.
- **Input Validation**: Custom validation ensuring clean financial data (e.g., non-negative amounts).
- **Advanced Reporting**: Uses Django ORM `annotate` and `Sum` to group and total expenses by category, with optional filtering by month/year.
- **Role-Based Permissions**: Only admin users can create or manage expense categories; regular users have read-only access to categories.
- **JWT Authentication**: Secure, token-based authentication using `djangorestframework-simplejwt`.
- **Test Coverage**: Core business logic (validation, permissions, reporting) is covered by automated tests.

## 🛠 Tech Stack

- **Language**: Python 3.x
- **Framework**: Django & Django REST Framework
- **Database**: SQLite (default)
- **Authentication**: JWT (`djangorestframework-simplejwt`)

## ⚙️ Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/mrmamadreza00/expense-tracker.git
cd expense-tracker
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. (Optional) Create a superuser to manage categories

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## 📚 API Endpoints

### Authentication

| Method | Endpoint                | Description                  |
|--------|--------------------------|-------------------------------|
| POST   | `/api/auth/register/`   | Register a new user           |
| POST   | `/api/auth/login/`      | Obtain JWT access/refresh tokens |
| POST   | `/api/auth/login/refresh/` | Refresh an access token    |

### Categories

| Method | Endpoint              | Description                          |
|--------|-------------------------|----------------------------------------|
| GET    | `/api/categories/`     | List all categories                    |
| POST   | `/api/categories/`     | Create a category (**admin only**)     |
| GET    | `/api/categories/{id}/`| Retrieve a single category              |
| PATCH  | `/api/categories/{id}/`| Update a category (**admin only**)      |
| DELETE | `/api/categories/{id}/`| Delete a category (**admin only**)      |

### Expenses

| Method | Endpoint                  | Description                                              |
|--------|-----------------------------|------------------------------------------------------------|
| GET    | `/api/expenses/`           | List the authenticated user's expenses                     |
| POST   | `/api/expenses/`           | Create a new expense                                        |
| GET    | `/api/expenses/{id}/`      | Retrieve a single expense                                    |
| PATCH  | `/api/expenses/{id}/`      | Update an expense                                             |
| DELETE | `/api/expenses/{id}/`      | Delete an expense                                              |
| GET    | `/api/expenses/summary/`   | Get spending totals grouped by category. Supports optional `?month=` and `?year=` query parameters. |

## 🔑 Authentication Example

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "ali", "email": "ali@test.com", "password": "yourpassword"}'

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "ali", "password": "yourpassword"}'
```

Use the returned `access` token in subsequent requests:

```
Authorization: Bearer <access_token>
```

## 🧪 Running Tests

```bash
python manage.py test
```

## 👨‍💻 Developed by

ممرضا | Backend Developer
