# TaskFlow — Django Full-Stack Task Manager

A full-stack, secure personal Task Manager web application built with **Python**, **Django 6.x**, **SQLite**, and **Bootstrap 5**.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-6.1-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## 🌟 Key Features

1. **User Authentication & Privacy**
   - User Registration (Signup with automatic login session).
   - Secure Login & Logout system using Django's built-in authentication framework.
   - **Server-Side Data Ownership**: All queries are filtered by `owner=request.user`.
   - **Strict Privacy Enforcement**: Unauthorized access attempts to other users' tasks return `HTTP 404 Not Found`.

2. **Full Task CRUD Operations**
   - **Create**: Add tasks with title, detailed description, due date picker, and status.
   - **Read**: Dashboard task list featuring summary statistics (Total, Pending, Completed, Overdue).
   - **Update**: Edit existing tasks with form pre-population.
   - **Delete**: Confirmation modal/page before task removal.
   - **Toggle Complete**: One-click completion status toggle directly from task cards.

3. **Modern Aesthetic UI**
   - Designed using **Bootstrap 5.3**, Font Awesome 6 icons, and custom CSS styling.
   - Google Font integration (`Plus Jakarta Sans`).
   - Summary statistics cards, custom status badges, search & status filter toolbar, and empty state layout.

---

## 📁 Project Structure

```
taskmanager/
├── manage.py
├── taskmanager/
│   ├── settings.py           # Installed apps, static files, templates config
│   ├── urls.py               # Root URL patterns (auth + tasks)
│   ├── wsgi.py
│   └── asgi.py
├── tasks/
│   ├── models.py             # Task model with User FK & ordering
│   ├── views.py              # Signup, task_list, task_create, task_update, task_delete, task_toggle
│   ├── urls.py               # Task routing
│   ├── forms.py              # TaskForm ModelForm with Bootstrap widgets
│   ├── admin.py              # Django Admin registration
│   ├── tests.py              # Comprehensive automated unit test suite (8 tests)
│   └── migrations/
│       └── 0001_initial.py
├── static/
│   └── css/
│       └── custom.css        # Metric cards, glassmorphic styles, status badges
├── templates/
│   ├── base.html             # Main layout, responsive navbar, flash alerts
│   ├── tasks/
│   │   ├── task_list.html    # Dashboard metrics, search filter, task list
│   │   ├── task_form.html    # Create/Edit task form
│   │   └── task_confirm_delete.html # Deletion confirmation
│   └── registration/
│       ├── login.html        # Login form
│       └── signup.html       # Signup form
└── README.md
```

---

## 🚀 Quick Setup & Installation Guide

### Prerequisites
- Python 3.10+ installed on your system.

### Step-by-Step Instructions

1. **Clone or navigate to the project directory:**
   ```bash
   cd taskmanager
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```cmd
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install django
   ```

4. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Automated Unit Tests:**
   ```bash
   python manage.py test tasks
   ```

6. **Start Local Development Server:**
   ```bash
   python manage.py runserver 8000
   ```

7. **Access the Application:**
   Open your browser and visit:  
   `http://127.0.0.1:8000/signup/`

---

## 🔒 Security Architecture Highlights

- **`@login_required` Decorators**: Applied to all protected task endpoints.
- **Query Ownership Filtering**: `Task.objects.filter(owner=request.user)` ensures no user can list another user's tasks.
- **`get_object_or_404(Task, pk=pk, owner=request.user)`**: Prevents unauthorized URL tampering. Attempting to view or manipulate another user's task ID yields a 404 response.
- **CSRF Tokens**: Embedded in all HTML forms (`{% csrf_token %}`).
- **Password Hashing**: Managed automatically by Django's PBKDF2 algorithm.

---

## 🧪 Verification & Testing Results

- **Automated Tests**: 8 unit tests covering signup, auto-login, task creation, editing, completion toggle, deletion, unauthenticated redirects, and cross-user 404 security checks.
- **All 8 tests passing OK**.
