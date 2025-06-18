# Intern Backend Project

This is a backend project built with **Django** and **Django REST Framework**. It includes API endpoints, JWT-based authentication, and monitoring tools like `django-silk`. The project is configured to run in a local environment using SQLite and `.env` for environment management.

---

## 🚀 Features

* Django 5.2.1 + DRF
* JWT Authentication (using `djangorestframework_simplejwt`)
* API documentation via Swagger (`drf-yasg`)
* Performance profiling with `django-silk`
* Modular and scalable app structure
* Git version-controlled project

---

---

## ⚙️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/intern_backend_project.git
   cd intern_backend_project
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**  
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**  
   ```bash
   python manage.py runserver
   ```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory and add the following (example):

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 🧪 Testing

You can write and run tests using:

```bash
python manage.py test
```

---

## 📦 Dependencies

Some major dependencies from `requirements.txt`:

```
asgiref==3.8.1
autopep8==2.3.2
Django==5.2.1
django-dirtyfields==1.9.7
django-silk==5.3.2
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
drf-yasg==1.21.10
```

---

---

## Author

**Tasin Mahmud**  

