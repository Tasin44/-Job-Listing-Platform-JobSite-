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
📘 API Endpoints
🔐 Authentication (/api/v1/auth/)
#### ✅ Register

    URL: /api/v1/auth/register/

    Method: POST

    Payload:

{
  "username": "user123",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword123",
  "confirm_password": "securepassword123"
}

    Response: 201 Created with user data

    Note: Alternatively, use /api/v1/auth/register/ with UserRegistrationSerializer for additional fields (phone, role) and JWT tokens.

🔑 Login

    URL: /api/v1/auth/login/

    Method: POST

    Payload:

{
  "email": "user@example.com",
  "password": "securepassword123"
}

    Response: 200 OK with user data and JWT tokens

🔓 Logout

    URL: /api/v1/auth/logout/

    Method: POST

    Payload:

{
  "refresh": "your-refresh-token"
}

    Response: 200 OK

♻️ Token Refresh

    URL: /api/v1/auth/token/refresh/

    Method: POST

    Payload:

{
  "refresh": "your-refresh-token"
}

    Response: 200 OK with new access token

🔁 Password Reset Request

    URL: /api/v1/auth/forgot-password/

    Method: POST

    Payload:

{
  "email": "user@example.com"
}

    Response: 200 OK

🔄 Password Reset Confirm

    URL: /api/v1/auth/reset-password/

    Method: POST

    Payload:

{
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123",
  "uid": "base64-encoded-uid",
  "token": "reset-token"
}

    Response: 200 OK

👤 User Profile

    URL: /api/v1/auth/profile/

    Method: GET, PUT, PATCH

    Response: 200 OK with profile data

    Authentication: Required

🙋 Current User

    URL: /api/v1/auth/me/

    Method: GET

    Response: 200 OK with user data

    Authentication: Required

💼 Jobs (/api/v1/jobs/)
📄 List Jobs

    URL: /api/v1/jobs/jobs/

    Method: GET

    Response: 200 OK with list of jobs

    Authentication: Required

    Note: Candidates see only active jobs; recruiters see their own jobs.

📝 Create Job

    URL: /api/v1/jobs/jobs/

    Method: POST

    Payload:

{
  "title": "Software Engineer",
  "description": "Develop web applications",
  "location": "Remote",
  "salary_min": 60000,
  "salary_max": 80000,
  "job_type": "FULL_TIME",
  "experience_level": "MID",
  "skills_required": "Python, Django, REST",
  "deadline": "2025-12-31T23:59:59Z"
}

    Response: 201 Created

    Authentication: Required (Recruiter only)

📌 Job Details

    URL: /api/v1/jobs/jobs/<pk>/

    Method: GET

    Response: 200 OK with job details

    Authentication: Required

✏️ Update/Delete Job

    URL: /api/v1/jobs/jobs/<pk>/

    Method: PUT, PATCH, DELETE

    Response: 200 OK or 204 No Content

    Authentication: Required (Recruiter owner only)

📥 Apply to Job

    URL: /api/v1/jobs/jobs/<pk>/apply/

    Method: POST

    Payload:

{
  "cover_letter": "I am excited to apply...",
  "resume": "<file-upload>"
}

    Response: 201 Created

    Authentication: Required (Candidate only)

🗃️ Job Applications (/api/v1/jobs/)
📃 List Applications

    URL: /api/v1/jobs/applications/

    Method: GET

    Response: 200 OK with list of applications

    Authentication: Required

    Note: Candidates see their own applications; recruiters see applications to their jobs.

🔍 Application Details

    URL: /api/v1/jobs/applications/<pk>/

    Method: GET

    Response: 200 OK with application details

    Authentication: Required

✅ Update Application Status

    URL: /api/v1/jobs/applications/<pk>/

    Method: PUT, PATCH

    Payload:

{
  "application_status": "ACCEPTED"
}

    Response: 200 OK

    Authentication: Required (Recruiter only)

❌ Delete Application

    URL: /api/v1/jobs/applications/<pk>/

    Method: DELETE

    Response: 204 No Content

    Authentication: Required (Owner only)

📊 Recruiter Dashboard
📈 Dashboard Stats

    URL: /api/v1/jobs/recruiter-dashboard/

    Method: GET

    Response: 200 OK with statistics (e.g., total jobs, applications, hires)

    Authentication: Required (Recruiter only)

📧 Email Configuration

The platform uses Django’s SMTP email backend to send notifications.
Current Gmail SMTP Config:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mdtm20062@gmail.com'
EMAIL_HOST_PASSWORD = 'lifbzbeazgtaxpkt'
DEFAULT_FROM_EMAIL = 'mdtm20062@gmail.com'

For Development:

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

🧪 Development Notes
🔁 Duplicate Registration Logic

    Consolidate to UserRegistrationSerializer by updating authapp/rest/urlss/urls.py

    Remove:

        authapp/rest/serializers/register.py

        authapp/rest/views/register.py

🔀 URL Configuration Fix

Replace incorrect import paths in config/urls.py with:

path("api/v1/auth/", include("authapp.rest.urlss.urls")),

📂 File Upload Validation

Add validators:

from django.core.validators import FileExtensionValidator

photo = models.ImageField(
    upload_to="profile_pictures/",
    blank=True,
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    help_text="Profile picture (JPG, JPEG, PNG)"
)

resume = models.FileField(
    upload_to="resumes/",
    blank=True,
    validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
    help_text="Resume/CV (PDF, DOC, DOCX)"
)

📨 Asynchronous Email Sending (with Celery)

from celery import shared_task

@shared_task
def send_welcome_email_task(user_id):
    user = User.objects.get(id=user_id)
    EmailService.send_welcome_email(user)

🌐 Root URL Redirect

Avoid 404 on root:

from django.shortcuts import redirect

def redirect_to_swagger(request):
    return redirect('/swagger/')

urlpatterns = [
    path('', redirect_to_swagger, name='home'),
    # ... other patterns ...
]

🚀 Future Improvements

    Consolidate duplicate registration logic

    Add email verification

    Write unit tests for critical endpoints

    Advanced job filtering (skills, salary)

    Integrate Celery for async tasks

    Rate limiting and CAPTCHA

    Job categories and tags

    Antivirus scanning for file uploads

🤝 Contributing

    Fork the repository

    Create a feature branch

git checkout -b feature/your-feature

Commit changes

git commit -m "Add your feature"

Push to the branch

    git push origin feature/your-feature

    Open a Pull Request
