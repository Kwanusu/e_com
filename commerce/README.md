# Commerce Project

This is a Django project for an online commerce platform, generated by `django-admin startproject` using Django 5.0.6.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tool (optional but recommended)
- PostgreSQL database
- Node.js and npm (for frontend, e.g., React)

## Installation

1. ## Clone the repository:

   git clone https://github.com/your-username/commerce.git
   cd commerce
### Create a virtual environment:


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the dependencies:


pip install -r requirements.txt
Set up the environment variables. Create a .env file in the project root and add the following:

## .env
create .env file in your root directory to store environment variables

SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
EMAIL_HOST_USER=your_email_host_user
EMAIL_HOST_PASSWORD=your_email_host_password
STRIPE_SECRET_KEY=your_stripe_secret_key

##  Apply the migrations:

# To migrate run the commands:

py manage.py makemigrations

python manage.py migrate

## Create a superuser:

python manage.py createsuperuser

## Collect static files:

python manage.py collectstatic

## Run the development server:

python manage.py runserver

**Configuration**
Settings
The main settings for the project are located in commerce/settings.py. Key settings include:

**BASE_DIR:** The base directory for the project.
**SECRET_KEY:** The secret key for the project, sourced from environment variables.
**DEBUG:** Debug mode setting (should be False in production).
**ALLOWED_HOSTS:** List of allowed hosts.
**DATABASES:** Database configuration, using dj_database_url to parse the DATABASE_URL from environment variables.
**EMAIL_BACKEND:** Email backend configuration for sending emails.
**CORS_ALLOWED_ORIGINS:** List of allowed origins for CORS.
**REST_FRAMEWORK:** Configuration for Django REST framework, including JWT authentication.
**SIMPLE_JWT:** Configuration for JWT tokens.

## Usage
Run the Django development server:

python manage.py runserver

Navigate to http://localhost:8000 to view the application.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/foo).
3. Make your changes.
4. Commit your changes (git commit -am 'Add some foo').
5. Push to the branch (git push origin feature/foo).
6. Open a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Your Name - kwanusujoseph@gmail.com

Joseph Kwanusu - LinkedIn

Project Link: https://github.com/Kwanusu/e_com.git
