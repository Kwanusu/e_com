## Commerce Project

An enterprise-grade e-commerce platform built with **Django 5.0.6**, featuring a robust REST API, JWT authentication, and Stripe payment integration.

## Table of Contents

  * [Prerequisites](https://www.google.com/search?q=%23prerequisites)
  * [Installation](https://www.google.com/search?q=%23installation)
  * [Configuration](https://www.google.com/search?q=%23configuration)
  * [Development](https://www.google.com/search?q=%23development)
  * [Contributing](https://www.google.com/search?q=%23contributing)
  * [License](https://www.google.com/search?q=%23license)

## Prerequisites

Ensure you have the following installed on your local machine:

  * **Python:** 3.10 or higher
  * **Database:** PostgreSQL
  * **Frontend Runtime:** Node.js & npm (if using React/Vue components)
  * **Tools:** Git, `pip`, and `venv`

## Installation

### 1\. Clone the repository

```bash
git clone https://github.com/Kwanusu/e_com.git
cd commerce
```

### 2\. Set up Virtual Environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root to store sensitive credentials:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/db_name
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
STRIPE_SECRET_KEY=sk_test_...
```

### Database & Static Files

Run the following commands to initialize the database and gather assets:

```bash
# Generate and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create administrative access
python manage.py createsuperuser

# Prepare static assets
python manage.py collectstatic
```

## Technical Overview

The architecture is designed for scalability and security, utilizing:

  * **Django REST Framework:** Powering the API layer.
  * **Simple JWT:** Secure, stateless authentication.
  * **CORS Headers:** Configured for cross-origin resource sharing with modern frontend frameworks.
  * **dj-database-url:** Utility to utilize `DATABASE_URL` environment variables for 12-factor app compliance.

## Development

To start the local development server:

```bash
python manage.py runserver
```

  * **API Root:** [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
  * **Admin Panel:** [http://localhost:8000/admin](https://www.google.com/search?q=http://localhost:8000/admin)

## Contributing

1.  **Fork** the repository.
2.  **Branch:** `git checkout -b feature/amazing-feature`.
3.  **Commit:** `git commit -m 'Add some amazing feature'`.
4.  **Push:** `git push origin feature/amazing-feature`.
5.  **Open a Pull Request.

## Contact

**Joseph Kwanusu** [Email](mailto:kwanusujoseph@gmail.com) | [LinkedIn](https://www.google.com/search?q=https://www.linkedin.com/in/joseph-kwanusu/) | [GitHub](https://www.google.com/search?q=https://github.com/Kwanusu)

**Project Link:** [https://github.com/Kwanusu/e\_com](https://www.google.com/search?q=https://github.com/Kwanusu/e_com)

*Licensed under the [MIT License](https://www.google.com/search?q=LICENSE).*
