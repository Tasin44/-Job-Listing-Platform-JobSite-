# JobSite Platform

JobSite is a comprehensive job listing platform built with Django and Django REST Framework. It supports role-based access control, allowing recruiters to post and manage job listings and candidates to apply for jobs. The platform includes user authentication, profile management, job application workflows, and email notifications, with a focus on scalability and maintainability.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Jobs](#jobs)
  - [Job Applications](#job-applications)
  - [Recruiter Dashboard](#recruiter-dashboard)
- [Email Configuration](#email-configuration)
- [Development Notes](#development-notes)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
JobSite is designed to facilitate job recruitment by providing a platform where recruiters can create and manage job postings, and candidates can browse and apply for jobs. The platform supports two user roles: Recruiter and Candidate, with role-based permissions to ensure secure access to features. Key functionalities include user registration, JWT-based authentication, job application management, and automated email notifications for registration, password resets, and job applications.

## Features

### User Authentication:
- Registration with email and password confirmation
- JWT-based login and token refresh
- Password reset via email
- User profile management with photo and resume uploads

### Job Management:
- Recruiters can create, update, and delete job postings
- Jobs include details like title, description, salary range, skills, and deadline
- Candidates can view active job listings and apply with cover letters and resumes

### Job Application Workflow:
- Candidates can submit applications to active jobs
- Recruiters can review applications and update statuses (e.g., Pending, Accepted, Rejected)
- Application tracking with unique identifiers

### Email Notifications:
- Welcome email upon registration
- Password reset emails
- Job application confirmations for candidates
- Application notifications for recruiters

### Role-Based Access Control:
- Recruiters can only manage their own jobs and applications
- Candidates can only view active jobs and their own applications

### API Documentation:
- Interactive Swagger UI (`/swagger/`) and Redoc (`/redoc/`) for API exploration

### Admin Interface:
- Django admin panel for managing users, jobs, and applications

### Performance Monitoring:
- Silk profiler for debugging and performance analysis (`/silk/`)

## Technologies
- **Backend**: Django 5.2.1, Django REST Framework
- **Authentication**: Django SimpleJWT for JWT-based authentication
- **Database**: SQLite (default, configurable for PostgreSQL/MySQL)
- **Email**: Django's SMTP backend (configured for Gmail)
- **API Documentation**: drf-yasg for Swagger and Redoc
- **Profiling**: django-silk for performance monitoring
- **File Storage**: Django's media storage for resumes and profile pictures
- **Dependencies**: Managed via `requirements.txt` (includes packages like django, djangorestframework, drf-yasg, django-silk, python-decouple)

## Project Structure
jobsite/
├── authapp/ # Authentication app
│ ├── rest/
│ │ ├── serializers/ # Serializers for API endpoints
│ │ │ ├── register.py # UserRegisterSerializer
│ │ │ └── serializers.py # Other serializers (login, profile, etc.)
│ │ ├── urlss/ # URL configurations
│ │ │ ├── register.py # Registration endpoint
│ │ │ ├── token.py # Token endpoints
│ │ │ └── urls.py # Main auth URLs
│ │ └── views/ # API views
│ │ ├── register.py # UserRegisterView
│ │ └── views.py # Other views (login, profile, etc.)
│ ├── signals.py # Signals for email notifications
│ ├── utils.py # EmailService and utility functions
│ └── apps.py # App configuration
├── core/ # Core app (models, managers, choices)
│ ├── admin.py # Admin interface for User, UserProfile
│ ├── choices.py # Enum choices (Gender, Role, Status)
│ ├── managers.py # Custom UserManager
│ ├── models.py # User, UserProfile models
│ ├── signals.py # Signal to create UserProfile
│ └── apps.py # App configuration
├── job/ # Job management app
│ ├── rest/
│ │ ├── serializers/ # Serializers for jobs and applications
│ │ │ └── serializers.py
│ │ ├── views/ # API views for jobs and applications
│ │ │ └── views.py
│ │ └── urls.py # Job-related URLs
│ ├── admin.py # Admin interface for Job, JobApplication
│ ├── choices.py # Enum choices (JobStatus, ApplicationStatus)
│ ├── models.py # Job, JobApplication models
│ ├── signals.py # Signals for application notifications
│ └── apps.py # App configuration
├── shared/ # Shared utilities
│ ├── base_admin.py # Base admin class
│ ├── base_model.py # Base model with UUID, timestamps
│ ├── choices.py # Shared status choices
│ └── permissions.py # Custom permissions
├── config/ # Project settings
│ ├── settings.py # Django settings
│ ├── urls.py # Root URL configuration
│ └── wsgi.py # WSGI entry point
├── media/ # Storage for uploaded files (resumes, photos)
└── manage.py # Django management script

## Setup Instructions

### 1. Clone the Repository:
```bash
git clone <repository-url>
cd jobsite
```
### 2. Create a Virtual Environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies:
Create a requirements.txt with the following content (adjust versions as needed):
```
django==5.2.1
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
drf-yasg==1.21.7
django-silk==5.1.0
python-decouple==3.8
django-dirtyfields==1.9.2
```
Then install:
bash
```
pip install -r requirements.txt
```
###4. Configure Environment Variables:

Create a .env file in the project root:
bash
```
touch .env
```
Add the following:
```
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```
Replace your-secret-key, your-email@gmail.com, and your-app-password with appropriate values. For Gmail, generate an App Password if 2FA is enabled.
###5. Apply Migrations:

```
python manage.py makemigrations
python manage.py migrate
```
###6. Create a Superuser:

```
python manage.py createsuperuser
```
## 7. Run the Development Server:

```
python manage.py runserver
```
Access the app at http://127.0.0.1:8000/.
Access Key URLs:

    Admin Panel: http://127.0.0.1:8000/admin/

    Swagger API Docs: http://127.0.0.1:8000/swagger/

    Redoc API Docs: http://127.0.0.1:8000/redoc/

    Silk Profiler: http://127.0.0.1:8000/silk/
