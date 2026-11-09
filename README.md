# WIL Placement Management System

IT Project Team 47, Richfield Graduate Institute of Technology.

A web-based system for managing Work Integrated Learning (WIL) placements, built with **Python 3, Django 5.2 (LTS) and MySQL 8**, following our Phase 4 System Design.

Students apply for placement opportunities and keep a logbook. Host organisations publish opportunities. Mentors sign off logbooks and evaluate students. Coordinators approve placements, capture results and run reports. Administrators approve new accounts and manage the system.

**Team:** Jaco van Niekerk · Amikar Motilal · Percy Maile · Khaya-Nkululeko Cele · Khanya Khoza · Tshepo Hlelesi

---

## Modules and owners

Each module is a Django app in `apps/`.

| App | Module | Main tables | Owner |
|---|---|---|---|
| `accounts` (models) | Database foundation: users, roles and profiles, audit log | `accounts_user`, `accounts_student`, `accounts_coordinator`, `accounts_mentor`, `accounts_employerprofile`, `audit_log` | Khaya-Nkululeko Cele |
| `accounts` (auth) | Login with email, logout, student registration with admin approval, role-based access, role start pages, session timeout | uses the tables above | Jaco van Niekerk |
| `organisations` | Host organisations and placement opportunities | `organisations_hostorganization`, `organisations_placementopportunity` | Tshepo Hlelesi |
| `placements` | Placement requests, approval and documents | `placement`, `document` | Khanya Khoza |
| `assessments` | Mentor evaluations and final results | `assessment`, `evaluation`, `assessment_result` | Khanya Khoza |
| `reports` | Coordinator reports | `report` | Khanya Khoza |
| `logbook` | Student logbook entries and mentor feedback | `logbook_entry` | Amikar Motilal |
| `students` | Student Portal: dashboard, profile and CV, opportunities, applications, notifications | `student_portal_profile`, `application`, `notification` | Percy Maile |
| `core` | Shared layout, home page, audit log and settings pages | none | Khanya Khoza / everyone |

Database models and `seed_all.py` sample data: Khaya-Nkululeko Cele.

---

## Roles and what each one sees

Everyone logs in at `/accounts/login/` with their **email address** and password. After login, each role goes straight to its own start page:

| Role | Start page | Can use |
|---|---|---|
| Student | `/students/` | Student Portal (profile, opportunities, applications, notifications), Logbook |
| Coordinator | `/placements/` | Placements, Assessments, Reports, Logbook |
| Mentor | `/logbook/` | Logbook (review and feedback) |
| Employer | `/organisations/` | Organisation dashboard; employers linked to an organisation can add placement opportunities |
| Administrator | `/admin/` (staff) | Django admin, approving new accounts, audit log, settings, placements, assessments, reports |

- **Registration:** new students register at `/accounts/register/`. The account stays inactive until an administrator approves it (tick **Active** on the user in `/admin/`).
- **Access control:** every module page requires login. A user with the wrong role gets **403 Forbidden**. Developers protect a view with:
  ```python
  from apps.accounts.decorators import role_required
  from apps.accounts.models import User

  @role_required(User.Role.COORDINATOR, User.Role.ADMIN)
  def my_view(request): ...
  ```
- **Session timeout:** users are logged out after 30 minutes without activity.

---

## Getting started

You need **Python 3.10+**, **Git** and (for MySQL) **MySQL Server 8+**.

### 1. Clone and install

**Windows (PowerShell)**
```powershell
git clone https://github.com/jacov677/IT-Project-Team-47.git
cd IT-Project-Team-47
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

**Mac / Linux**
```bash
git clone https://github.com/jacov677/IT-Project-Team-47.git
cd IT-Project-Team-47
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`requirements.txt` includes `mysqlclient`. On a Mac, if it fails to install, run `brew install mysql pkg-config` first.

### 2. Choose a database

**MySQL (the project database, Phase 4 section 4.4.6).** In MySQL Workbench, connected as root, run (choose your own password):
```sql
CREATE DATABASE IF NOT EXISTS wil_placement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'wil_app'@'localhost' IDENTIFIED BY 'your-password';
CREATE USER IF NOT EXISTS 'wil_app'@'127.0.0.1' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON wil_placement.*      TO 'wil_app'@'localhost', 'wil_app'@'127.0.0.1';
GRANT ALL PRIVILEGES ON test_wil_placement.* TO 'wil_app'@'localhost', 'wil_app'@'127.0.0.1';
FLUSH PRIVILEGES;
```
Then set these lines in `.env`:
```
DB_ENGINE=mysql
DB_NAME=wil_placement
DB_USER=wil_app
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

**SQLite (quick start, nothing to install):** leave `DB_ENGINE=sqlite` in `.env`.

### 3. Create the tables and an administrator

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000 and log in with the superuser's email and password.

### 4. Load sample data (optional)

```bash
python seed_all.py
```
This creates organisations, users, placements, documents, logbook entries, assessments, evaluations, results and reports. It is safe to run more than once, and only runs when `DJANGO_DEBUG=True`.

All sample users have the password **`Test@12345`**:

| Email | Role |
|---|---|
| `ayesha@test.co.za`, `lwazi@test.co.za`, `risto@test.co.za`, `bongani@test.co.za`, `zanele@test.co.za` | Student |
| `thandi@test.co.za`, `nkule@test.co.za` | Coordinator |
| `sipho@test.co.za`, `naledi@test.co.za` | Mentor |
| `admin@test.co.za` | Administrator (use your superuser for `/admin/`) |

To see opportunities in the Student Portal, add a **Placement opportunity** in `/admin/` (or as an employer linked to that organisation).

---

## Running the tests

```bash
python manage.py test
```
The suite has **48 tests** covering login, registration and approval, role-based access, role start pages, session timeout, and the Student Portal (applying, withdrawing, notifications, profile). GitHub Actions runs the tests and checks for missing migrations on every push and pull request.

---

## Project structure

```
config/             settings.py and the main urls.py
apps/
  accounts/         users, roles, profiles, login, registration, role_required
  organisations/    host organisations and placement opportunities
  placements/       placements, approval and documents
  logbook/          logbook entries and mentor feedback
  assessments/      evaluations and final results
  reports/          coordinator reports
  students/         Student Portal
  core/             home page, audit log, settings
templates/          base.html (shared layout and navigation)
static/             CSS and Bootstrap 5
seed_all.py         sample data for development
```

Security notes: passwords are stored hashed by Django, all forms use CSRF protection, logout only works through a POST form, and secrets live in `.env` (never committed). See `CONTRIBUTING.md` for how we use branches, pull requests and migrations.
