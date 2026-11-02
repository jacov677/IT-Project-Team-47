# WIL Placement Management System

IT Project Team 47, Richfield Graduate Institute of Technology.

A web-based system for managing Work Integrated Learning (WIL) placements, built with **Python and Django 5.2**, following our Phase 4 System Design.

**Team:** Jaco van Niekerk · Amikar Motilal · Percy Maile · Khaya-Nkululeko Cele · Khanya Khoza · Tshepo Hlelesi

This repository is a **skeleton**. The project runs and has one empty app per module. Each team member builds their own module inside their own app.

---

## Getting started

You need **Python 3.10+** and **Git**.

**Windows (PowerShell)**
```powershell
git clone https://github.com/jacov677/IT-Project-Team-47.git
cd IT-Project-Team-47
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

**Mac / Linux**
```bash
git clone https://github.com/jacov677/IT-Project-Team-47.git
cd IT-Project-Team-47
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000. The home page links to every module's start page.

The project uses SQLite by default, so there is nothing else to install. To switch to MySQL later, set `DB_ENGINE=mysql` and the `DB_` values in `.env`, then run `pip install mysqlclient`.

---

## Modules and owners

Each module is a Django app in `apps/`. Agree on owners as a group and fill in the table.

| App | Module | Phase 4 tables (section 4.5) | Owner |
|---|---|---|---|
| `accounts` | Login, registration, roles, profiles | user, student, coordinator, mentor | |
| `organisations` | Host organisations | host_organization | |
| `placements` | Placement requests, approval, documents | placement, document | |
| `logbook` | Logbook entries and mentor sign-off | logbook_entry | |
| `assessments` | Mentor evaluations and final results | evaluation, assessment_result | |
| `reports` | Coordinator reports and audit log | audit_log | |
| `core` | Shared layout and home page | none | everyone |

**Build `accounts` first.** The other modules need the user and profile models (Student, Mentor, Coordinator), so those should be in place before others add foreign keys to them.

---

## Project structure

```
config/          settings.py and the main urls.py
apps/
  core/          home page
  accounts/      ┐
  organisations/ │
  placements/    │  one app per module, each with:
  logbook/       │    models.py, views.py, urls.py, admin.py, tests.py
  assessments/   │    templates/<app>/index.html  (placeholder start page)
  reports/       ┘
templates/       base.html (shared layout and navigation)
static/          CSS and Bootstrap 5
```

To add a page to your module:
1. Write the view in `apps/<your_app>/views.py`.
2. Add it to `apps/<your_app>/urls.py`.
3. Create the template in `apps/<your_app>/templates/<your_app>/` and start it with `{% extends "base.html" %}`.

See **CONTRIBUTING.md** for how we use branches, pull requests and migrations.
