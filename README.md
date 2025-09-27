# 🏛️ Auditorium Booking System (Flask & TiDB)

> This project is a robust, full-stack application built with **Flask** and **SQLAlchemy**. It facilitates the scheduling and conflict resolution for a college auditorium, featuring user-facing appointment booking and a secure, time-sensitive admin dashboard for management. [cite\_start]The system is designed with a focus on modularity, security, and using **TiDB** as the persistent SQL backend[cite: 253].

-----

## Project File Directory Structure

The project uses a clear, modular structure following the Flask application factory pattern:

```
AUDITORIUM/
├── __pycache__
├── static/
├── templates/
│   ├── about.html
│   ├── admin_login.html
│   ├── admin.html
│   ├── base.html
│   ├── book_appointment.html
│   ├── dashboard.html
│   └── home.html
├── venv/
├── .env
├── .gitignore
├── __init__.py         <-- Flask App Factory
├── app.py              <-- Entry point to run the server
├── config.py           <-- Configuration settings (DB URI, SECRET_KEY)
├── handler.py          <-- Business logic handlers (e.g., booking logic)
├── models.py           <-- SQLAlchemy Database Models
├── requirements.txt
├── resume.html         <-- (Auxiliary file)
├── routes.py           <-- All URL endpoint definitions
├── run_app.py
├── run.py
└── store.txt
```

-----

## Technology Stack

  * [cite\_start]**Core Framework**: **Flask** [cite: 210, 231]
  * [cite\_start]**Database ORM**: **Flask-SQLAlchemy** [cite: 211]
  * [cite\_start]**Database Backend**: **TiDB Cloud** (Tested via `test-connection` route) [cite: 253]
  * [cite\_start]**Deployment/Config**: **`.env`** file (for environment variables and secrets) [cite: 285]
  * **Security & Features**: Password Hashing (`werkzeug.security`), **Flask-Limiter** (Implied for brute-force protection), Session Management.

-----

## Core Components and Initialization

### 1\. Application Factory (`__init__.py`)

[cite\_start]This file implements the **Factory Pattern** (`create_app()`), allowing the application to be more modular and testable[cite: 215].

  * [cite\_start]**Initialization:** It initializes the Flask app, loads configuration from `config.py`, and registers the **SQLAlchemy instance** (`db.init_app(app)`)[cite: 214].
  * [cite\_start]**Database Setup:** It uses `db.create_all()` within the application context (`with app.app_context():`) to automatically create the database tables if they do not already exist[cite: 218].
  * [cite\_start]**Route Handling:** It imports all routes (`import routes`) at the end to prevent **circular import issues**[cite: 222, 223].

### 2\. Database Models (`models.py`)

[cite\_start]This file defines four core tables using the SQLAlchemy ORM[cite: 264]:

| Model | Purpose | Key Columns & Features |
| :--- | :--- | :--- |
| **User** | [cite\_start]Stores user details and event request information[cite: 266]. | [cite\_start]`id` (PK), `name`, `institute_name`, `event_details`, `expected_turnover`, `request_date`[cite: 266, 268]. |
| **Appointment** | [cite\_start]Stores the scheduled booking records[cite: 269]. | [cite\_start]`id` (PK), `name`, `institute_name`, `appointment_date`, `status` (Default: "Pending")[cite: 270, 271, 272]. |
| **Admin** | Stores administrator credentials. | [cite\_start]`id` (PK), `name`, `password_hash`[cite: 273, 274]. [cite\_start]Includes `set_password` and `check_password` methods using secure password hashing[cite: 275]. |
| **Session** | Manages admin authentication state. | [cite\_start]`id` (PK), `admin_id` (FK to `Admin`), `session_token` (Unique), `created_at`[cite: 277, 278]. |

-----

## API Routes and Functionality (`routes.py`)

The application defines several routes to manage public bookings, display information, and handle secure admin management.

### Public Routes (User and Information)

| Method | Endpoint | Description | Database Action |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | [cite\_start]**Home Page:** Displays scheduled appointments[cite: 240, 241]. | [cite\_start]Queries all appointments, sorted by date (`Appointment.query.order_by...`)[cite: 240]. |
| **GET, POST**| `/book-appointment` | [cite\_start]Displays the booking form (`GET`) or processes the booking request (`POST`) by calling the dedicated `book_appointment_handler()`[cite: 243]. | Data is handled by `handler.py`. |
| **GET** | `/view-appointments`| [cite\_start]Lists all appointments with their details (ID, Name, Status, Date)[cite: 251]. | Queries all appointments (`Appointment.query.all()`). |
| **GET** | `/test-connection`| [cite\_start]Checks the active connection to the TiDB server[cite: 253]. | [cite\_start]Executes a raw SQL query: `SELECT VERSION()`[cite: 254]. |
| **GET** | `/about` | [cite\_start]Renders the `about.html` template[cite: 255]. | None. |

### Admin Protected Routes

All routes accessing administrative functions are secured with a session check (`if "admin_id" not in session`). [cite\_start]The system also enforces **session expiry**[cite: 306].

| Method | Endpoint | Description | Security Features |
| :--- | :--- | :--- | :--- |
| **GET, POST**| `/admin/login` | Login page. [cite\_start]Redirects to `/dashboard` if the admin is already logged in[cite: 244]. | [cite\_start]Uses handlers to verify credentials and set the session token/expiry[cite: 305]. |
| **GET** | `/dashboard` | Main admin panel. [cite\_start]Lists **all** appointments for review[cite: 246]. | [cite\_start]**Session Check:** Logs out and redirects if the session is expired[cite: 306]. |
| **POST** | `/approve-appointment/<id>`| [cite\_start]Approves a specific appointment by ID[cite: 248]. | [cite\_start]Updates the `status` column to **"approved"** and commits to the database[cite: 249]. |
| **GET** | `/admin` | [cite\_start]Displays the main admin page (`admin.html`)[cite: 256]. | [cite\_start]Requires `admin_id` in session; flashes a warning if unauthorized[cite: 257]. |
