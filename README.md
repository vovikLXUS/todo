# TODO List Application

A web application for task tracking and organization built with Python and Django, styled with Bootstrap 5.

---

## Project Overview

### Task Description
The goal of this project is to implement a functional TODO List web application that enables users to manage daily tasks, set deadlines, organize items using customizable tags, and track completion progress in an intuitive user interface.

### Functional Requirements and Features
* Task Management:
  * Content: Each task has a textual description detailing what needs to be done.
  * Creation Timestamp: Automatically recorded creation date and time (`created_at`).
  * Deadline: Optional due date and time field (`deadline`) using an HTML5 datetime-local picker.
  * Status Tracking: Boolean indicator (`is_done`) displaying whether the task is completed or active.
  * Tag Association: Many-to-many relationship allowing tasks to have multiple tags and tags to be reused across tasks.
  * Task Ordering: Tasks are sorted with incomplete tasks at the top, and within each status group ordered from newest to oldest (`["is_done", "-created_at"]`).
  * Quick Status Toggle: Direct "Complete" / "Undo" action on the home page that instantly toggles task completion status and refreshes the view.
  * Task CRUD: Complete support for creating, viewing, editing, and deleting tasks with a confirmation step on deletion.

* Tag Management:
  * Identification: Each tag has a unique name.
  * Tag Catalog: Dedicated page listing all tags in a clean tabular view.
  * Tag CRUD: Complete support for creating new tags, updating existing tags, and deleting tags with deletion confirmation.

* Navigation and User Interface:
  * Persistent Sidebar: Accessible across all pages with direct links to "Home" and "Tags".
  * Bootstrap 5 Styling: Clean, responsive layout with visual badges for task status ("Done" in green, "Not done" in red).
  * Django Debug Toolbar: Integrated in the development environment for query inspection and performance monitoring.

---

## Repository Architecture

### Directory Tree
```
todo/
|-- tasks/
|   |-- migrations/
|   |   `-- 0001_initial.py         # Initial database migration for Tag and Task
|   |-- admin.py                    # Django admin configuration for models
|   |-- apps.py                     # Tasks application configuration
|   |-- forms.py                    # Form definitions (TaskForm, TagForm)
|   |-- models.py                   # Data models (Tag, Task)
|   |-- tests.py                    # Unit and integration test suite (13 tests)
|   |-- urls.py                     # Application routing and URL patterns
|   `-- views.py                    # Class-based and generic views for tasks and tags
|-- templates/
|   |-- includes/
|   |   `-- sidebar.html            # Global sidebar navigation partial
|   |-- tasks/
|   |   |-- index.html              # Home page: list of tasks with toggle buttons
|   |   |-- tag_confirm_delete.html # Confirmation page for tag deletion
|   |   |-- tag_form.html           # Form page for creating and updating tags
|   |   |-- tag_list.html           # Table view of all registered tags
|   |   |-- task_confirm_delete.html# Confirmation page for task deletion
|   |   `-- task_form.html          # Form page for creating and updating tasks
|   `-- base.html                   # Master layout template (Bootstrap, sidebar, content block)
|-- todo_list/
|   |-- asgi.py                     # ASGI application entrypoint
|   |-- settings.py                 # Project settings (loads .env configuration)
|   |-- urls.py                     # Root URL dispatcher
|   `-- wsgi.py                     # WSGI application entrypoint
|-- .env.example                    # Environment variables template
|-- .gitignore                      # Git ignore file
|-- manage.py                       # Django CLI management script
|-- README.md                       # Project documentation
`-- requirements.txt                # Project Python dependencies
```

### Architectural Components
* `tasks/models.py`: Defines the database schema:
  * `Tag`: Stores unique category tags, ordered alphabetically by name.
  * `Task`: Stores task text, creation time, optional deadline, status flag, and many-to-many relationship with tags.
* `tasks/views.py`: Implements Django generic Class-Based Views:
  * `TaskListView`: Lists all tasks, optimizing queries with `prefetch_related("tags")`.
  * `TaskCreateView` / `TaskUpdateView` / `TaskDeleteView`: Standard CRUD operations for tasks.
  * `TaskToggleStatusView`: Handles one-click status inversion (toggling `is_done`) for both GET and POST requests.
  * `TagListView` / `TagCreateView` / `TagUpdateView` / `TagDeleteView`: Standard CRUD operations for tags.
* `tasks/forms.py`:
  * `TaskForm`: Configures datetime input widget for deadline and multiple checkbox selection for tags.
  * `TagForm`: Form for tag creation and editing with Bootstrap form control styling.
* `tasks/tests.py`: Comprehensive test suite testing model string representations, custom ordering, helper properties, and all views/endpoints.
* `todo_list/settings.py`: Configured to dynamically read sensitive configuration (`SECRET_KEY`) and execution mode (`DEBUG`) from the environment via `python-dotenv`.

---

## Local Setup and Installation

Follow the steps below to set up and run the project on your local machine.

### 1. Fork the Repository
1. Navigate to the project repository on GitHub.
2. Click the "Fork" button in the upper-right corner of the page.
3. Select your GitHub account as the destination to create your personal fork.

### 2. Clone the Forked Repository
Clone your fork to your local system:
```bash
git clone https://github.com/<your-username>/todo.git
cd todo
```

### 3. Create and Activate a Virtual Environment

* On Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

* On Windows (Command Prompt):
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

* On Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` configuration file from the provided `.env.example` template:

* On Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

* On Linux / macOS / Git Bash:
```bash
cp .env.example .env
```

Open `.env` in a text editor and configure your variables:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 6. Apply Database Migrations
Run Django migrations to create SQLite database tables:
```bash
python manage.py migrate
```

### 7. Create a Superuser (Optional)
If you wish to access the Django admin panel (`/admin/`), create an administrative account:
```bash
python manage.py createsuperuser
```
Follow the interactive prompt to enter your username, email, and password.

### 8. Run the Automated Tests
Verify that all unit and integration tests pass:
```bash
python manage.py test
```

### 9. Start the Development Server
Launch the Django local development server:
```bash
python manage.py runserver
```

Once started, navigate to the following URL in your web browser:
http://127.0.0.1:8000/