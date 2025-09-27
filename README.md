
# Flask-based Auditorium Booking System

> Hi, I'm Kushal K. This repository contains a Flask web application designed to manage college auditorium bookings. It provides user-friendly interfaces for booking, and an admin dashboard to approve and manage requests. The system uses SQLAlchemy ORM for database management and TiDB Cloud as the backend database.

---

## Core Components

- [File Directory Structure](#file-directory-structure)  
- [Instructions to Run the Code](#instructions-to-run-the-code)  
- [Initialization (`__init__.py`)](#initialization-__init__py)  
- [Application Entrypoint (`app.py`)](#application-entrypoint-apppy)  
- [Routes (`routes.py`)](#routes-routespy)  
- [Models (`models.py`)](#models-modelspy)  
- [Configuration (`config.py`)](#configuration-configpy)  
- [Admin Login & Security](#admin-login--security)  
- [Templates & Static Files](#templates--static-files)  
- [Scalability and Enhancements](#scalability-and-enhancements)  

---

## File Directory Structure

```text
AUDITORIUM/
├── static/
├── templates/
│   ├── about.html
│   ├── admin_login.html
│   ├── admin.html
│   ├── base.html
│   ├── book_appointment.html
│   ├── dashboard.html
│   └── home.html
├── .env
├── .gitignore
├── __init__.py
├── app.py
├── config.py
├── handler.py
├── models.py
├── requirements.txt
├── routes.py
├── run_app.py
└── run.py
````

---

## Technology Stack

* **Framework:** Flask
* **Database:** TiDB Cloud (via SQLAlchemy ORM)
* **Authentication & Security:** Flask-Session, Werkzeug Security (password hashing), Flask-Limiter (rate limiting)
* **Frontend:** HTML (Jinja2 templates), Bootstrap for styling
* **Core Language:** Python

---

## Project Architecture

```mermaid
flowchart TD
    User[User] -->|Book Appointment| FlaskApp[Flask Application]
    Admin[Admin] -->|Login / Manage| FlaskApp
    FlaskApp -->|ORM| DB[(TiDB Cloud Database)]
    DB --> FlaskApp
    FlaskApp --> Templates[HTML Templates + Static Files]
```

The application follows a modular Flask architecture:

1. **Initialization (`__init__.py`)**: Creates the Flask app, configures SQLAlchemy, sets up error handling, and imports routes.
2. **Routes (`routes.py`)**: Defines user and admin routes (home, booking, login, dashboard, etc.).
3. **Models (`models.py`)**: Defines User, Appointment, Admin, and Session tables using SQLAlchemy ORM.
4. **Config (`config.py`)**: Loads environment variables like DB URI and secret key from `.env`.
5. **Handler (`handler.py`)**: Processes booking and admin requests.
6. **Templates:** HTML files for UI (home, dashboard, booking, admin login).

---

## In-Depth Component Explanations

### Initialization (`__init__.py`)

* Uses **Factory Pattern (`create_app`)** for modularity and testing.
* Sets up **SQLAlchemy** connection with TiDB.
* Auto-creates tables if they don’t exist (`db.create_all()`).
* Handles circular imports by importing routes after app creation.

### Application Entrypoint (`app.py`)

* Imports the app instance from `__init__.py`.
* Runs the server with `debug=True` (development mode).

### Routes (`routes.py`)

Defines key routes:

* `/` → Home page with appointment list.
* `/book-appointment` → Booking form (GET/POST).
* `/admin/login` → Admin login page.
* `/dashboard` → Admin dashboard (secure).
* `/approve-appointment/<id>` → Approve appointment (admin only).
* `/view-appointments` → View all bookings.
* `/test-connection` → Check TiDB connection.
* `/about` → About page.

### Models (`models.py`)

SQLAlchemy ORM models:

* **User**: Stores applicant info (name, institute, event details).
* **Appointment**: Stores booking info with status (Pending/Approved).
* **Admin**: Stores admin credentials with **hashed passwords**.
* **Session**: Manages secure admin sessions with tokens.

### Configuration (`config.py`)

* Loads secrets from `.env`.
* Configures `SQLALCHEMY_DATABASE_URI`, `SECRET_KEY`, and debug mode.
* Ensures sensitive data is not hardcoded.

### Admin Login & Security

* Implements **Flask-Limiter** to prevent brute-force login attempts (5 per minute).
* Uses **session tokens with expiry** (30 min auto logout).
* Passwords stored securely with **hashing**.

### Templates & Static Files

* `templates/` contains HTML pages for users and admins.
* `static/` folder holds CSS, JS, and assets.
* `base.html` used for template inheritance.

---

## Scalability and Enhancements

* **Scalability**:

  * Modular codebase → easy to integrate Blueprints.
  * Database can scale horizontally (TiDB).
  * Session tokens allow for secure distributed admin login.

* **Enhancements Suggested**:

  * Use **Flask-Migrate** for database migrations.
  * Restrict `/test-connection` to admin users only.
  * Add indexes for faster query performance.
  * Add automated appointment reminders via email/SMS APIs.

---

## Instructions to Run the Code

### Prerequisites

* [Python 3.9+](https://www.python.org/downloads/) installed.
* Virtual environment (`venv`) created.
* TiDB Cloud or any SQL database setup with URI.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/kushalk47/auditorium-booking
   cd auditorium-booking
   ```

2. **Create Virtual Environment & Install Dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup Environment Variables**
   Create a `.env` file in the root folder:

   ```
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@host/dbname
   ```

4. **Run the Application**

   ```bash
   python app.py
   ```

5. **Access the Application**

   * User homepage: **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**
   * Admin dashboard: **[http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard)**

---

```





