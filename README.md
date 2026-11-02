# WIL Placement Management System

IT Project Team 47, Richfield Graduate Institute of Technology.

This is a web-based system for managing Work Integrated Learning (WIL) placements. Students log their placement work, mentors sign it off and evaluate it, WIL coordinators approve placements and capture final results, and administrators manage accounts. It is built with **Python, Django 5.2 (LTS) and MySQL 8.0**, as specified in our Phase 4 System Design.

**Team:** Jaco van Niekerk · Amikar Motilal · Percy Maile · Khaya-Nkululeko Cele · Khanya Khoza · Tshepo Hlelesi

---

## 1. What is already built

| Area | Status |
|---|---|
| All 11 database tables from Phase 4 section 4.5, with the same table and column names, keys and constraints | Done |
| Email login, hashed passwords, inactive accounts blocked until an admin activates them | Done |
| Server-side role checks (`role_required`, `RoleRequiredMixin`) | Done |
| A dashboard for each role: Student, Mentor, Coordinator, Admin | Done (read-only) |
| Business rules as service functions (placements, logbook, evaluations, final results) | Done and tested |
| Audit log of every create, update and approval | Done |
| Protected document download (files stored outside the web root, permission-checked) | Done |
| Django admin site for every table | Done |
| Demo data command so everyone has the same test accounts | Done |
| 30 automated tests and a GitHub check that runs them on every pull request | Done |
| **Forms and pages for each module** | **To build: see section 6** |

---

## 2. First-time setup

You need **Python 3.10+**, **Git** and **MySQL 8.0**.
On Windows, install MySQL with the [MySQL Installer](https://dev.mysql.com/downloads/installer/) and choose "Server only".

### 2.1 Clone and create a virtual environment

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

> Mac: if `mysqlclient` fails to install, run `brew install mysql pkg-config` first.
> Linux: `sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config`.

### 2.2 Create the database

Open `docs/mysql_setup.sql` and change the password on the `CREATE USER` line. Then run:

```bash
mysql -u root -p < docs/mysql_setup.sql
```

Put the same password in your `.env` file as `DB_PASSWORD`.

> **No MySQL yet?** Set `DB_ENGINE=sqlite` in `.env` to start immediately. Switch back to MySQL before you open a pull request.

### 2.3 Create the tables, load demo data and run

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000 and log in with any demo account. **Password for all of them: `WilDemo#2026`**

| Email | Role |
|---|---|
| admin@wil.test | Administrator (also opens the Django admin site at /admin) |
| coordinator@wil.test | WIL Coordinator |
| mentor@wil.test | Mentor |
| student1@wil.test | Student with an active placement and logbook entries |
| student2@wil.test | Student with a pending placement |
| newstudent@wil.test | Inactive account (shows the login block) |

### 2.4 Run the tests

```bash
python manage.py test
```

Run them before every pull request. GitHub also runs them automatically against MySQL 8.0.

---

## 3. Project structure

```
config/              Django settings and main URLs
apps/
  core/              Dashboards, shared helpers, demo data command, test helpers
  accounts/          user, student, coordinator, mentor tables; login; role permissions
  organisations/     host_organization table
  placements/        placement and document tables; protected downloads
  logbook/           logbook_entry table
  assessments/       evaluation and assessment_result tables
  audit/             audit_log table and log_action()
templates/           HTML pages (Bootstrap 5)
static/              CSS and images
docs/                MySQL setup script
```

Each app follows the same pattern:

| File | What goes in it |
|---|---|
| `models.py` | Tables. **Do not rename tables or columns**; they match section 4.5. |
| `services.py` | Business rules. Views call these and never change the database directly for rule-bound actions. |
| `forms.py` | Django forms for input validation (section 4.7 Input Design). |
| `views.py` / `urls.py` | Pages. Protect every view with `@role_required(...)`. |
| `tests/` | Tests for that app. Use the helpers in `apps/core/testing.py`. |

### Using the service functions in a view

```python
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from apps.accounts.models import Role
from apps.accounts.permissions import role_required
from apps.core.exceptions import BusinessRuleError
from apps.logbook.models import LogbookEntry
from apps.logbook.services import sign_off_entry


@role_required(Role.MENTOR)
def sign_off(request, pk):
    entry = get_object_or_404(LogbookEntry, pk=pk)
    try:
        sign_off_entry(request.user, entry)   # checks it is the assigned mentor, audits it
        messages.success(request, "Entry signed off.")
    except BusinessRuleError as error:
        messages.error(request, error.message)
    return redirect("placements:detail", pk=entry.placement_id)
```

---

## 4. Business rules (Phase 4, sections 4.1 and 4.5)

| Rule | Where it is enforced |
|---|---|
| A student can only have one open placement | `placements/services.py` (`create_placement`, `approve_placement`) |
| No logbook entries before the placement is approved | `logbook/services.py` (`submit_entry`) |
| Only the assigned mentor signs off entries and submits the evaluation | `logbook/services.py`, `assessments/services.py` |
| Signed-off entries cannot be edited unless the mentor reopens them (audited) | `logbook/services.py` (`edit_entry`, `reopen_entry`) |
| A final result needs every entry signed off and the evaluation submitted | `assessments/services.py` (`capture_final_result`) |
| One evaluation and one final result per placement | Unique keys in the database and checks in the services |
| Final mark 0 to 100; hours 0 to 24; end date after start date | Database CHECK constraints |
| Every create, update and approval is audited | `audit/services.py` (`log_action`) |
| Passwords hashed; documents only downloadable by permitted users | Django auth; `placements/views.py` |

---

## 5. Settings and secrets

All secrets live in `.env`, which is **never committed** (section 4.4.8). Uploaded documents are saved under `protected_media/` (or `DOCUMENT_STORAGE_PATH`) and are only served through the permission-checked download view. Allowed types are PDF, DOCX, JPG and PNG, up to 10 MB.

Production settings (HTTPS-only cookies, HSTS, SSL redirect) switch on automatically when `DJANGO_DEBUG=False`. Gunicorn and Nginx are used on the server (section 4.4.6).

---

## 6. Work still to do

Suggested split: one module per person. Agree on owners in the group and fill in the table.

| Module | Pages to build | Owner |
|---|---|---|
| Accounts | Registration (account starts inactive), profile edit, password reset, admin activation page | |
| Organisations and mentors | Add or edit host organisations and mentor profiles (coordinator) | |
| Placements | Create placement, coordinator approve or reject, document upload | |
| Logbook | Submit and edit entries (student); sign off and reopen (mentor) | |
| Assessments | Mentor evaluation form; coordinator final result capture | |
| Reports and UI | Coordinator reports (placement summary, logbook progress, results), navigation, styling | |

The service functions and tests for each module already exist. Most of the remaining work is forms, views and templates.

See **CONTRIBUTING.md** for how we use branches, pull requests and migrations.

### Open design question

Section 4.5 has no Employer role or Application table, so host organisations are represented by their mentors. Section 4.7 still describes an Employer dashboard. If the group adds them, update section 4.5 first, then add the models and one migration in a single pull request.
