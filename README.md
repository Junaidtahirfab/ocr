# ocr
# Django REST Framework Project

This project is built using Django REST Framework and is designed to serve as a backend for web applications. It includes a set of APIs for managing data and interacting with various services.

## Requirements

Ensure you have the following installed:

- Python 3.10
- Django 4.2.14
- Django REST Framework 3.15.2

## Installation and Setup

### 1. Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone <your-repository-url>
cd <your-project-directory>
```

### 2. Create and Activate Virtual Environment
Create a virtual environment and activate it:
```bash
python3.8 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
Install the necessary dependencies from the requirements.txt file:
```bash
pip install -r requirements.txt
```
### 4. Database Migrations
Make and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Create a Superuser
(Optional) Create a superuser to access Django Admin:
```bash
python manage.py createsuperuser
```

## Running the Project

### Start the Django Development Server
#### To start the Django development server, run:
```bash
python manage.py runserver
```
The server will be available at http://127.0.0.1:8000/.


# Additional Information

## Environment Variables
Ensure all required environment variables are set, including DATABASE_URL, SECRET_KEY, and any other configuration specific to your setup.

# License
This project is licensed under the MIT License - see the LICENSE file for details.