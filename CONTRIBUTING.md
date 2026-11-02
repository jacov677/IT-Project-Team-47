# How we work together

Six people share this code, so these rules keep `main` working for everyone.

## 1. Never commit straight to `main`

```bash
git checkout main
git pull                                   # get everyone's latest work
git checkout -b feature/logbook-submit     # one branch per task
# ...write code and tests...
git add .
git commit -m "Add logbook entry form for students"
git push -u origin feature/logbook-submit
```

Then open a **pull request** on GitHub. Another team member reviews it, the automatic tests must pass, and then it is merged.

Branch names: `feature/<what>`, `fix/<what>`, `docs/<what>`.

## 2. Keep your branch up to date

Before you open a pull request, and at least every few days:

```bash
git checkout main
git pull
git checkout feature/your-branch
git merge main
python manage.py migrate
python manage.py test
```

## 3. Migrations (the most common team problem)

- Only change `models.py` in **your own module**. If you need a change in someone else's module, ask them first.
- After changing a model: `python manage.py makemigrations <app>`, then commit the new migration file **with** the model change.
- **Never edit or delete a migration that is already on `main`.** Make a new one instead.
- If two people create migrations at the same time, Django will say "Conflicting migrations". Pull `main`, then run `python manage.py makemigrations --merge`.
- Do not rename tables or columns. They match Phase 4 section 4.5 and the ERD.

## 4. Rules for code

- Every view needs a role check: `@role_required(Role.MENTOR)` or `RoleRequiredMixin`.
- Business rules go in `services.py`, not in views or templates.
- Every create, update or approval calls `log_action(...)`. The existing services already do this.
- Add at least one test for every new service function or page.
- Never commit `.env`, passwords, the database or uploaded files. `.gitignore` already blocks them.

## 5. Pull request checklist

- [ ] `python manage.py test` passes
- [ ] `python manage.py makemigrations --check` says "No changes detected"
- [ ] The page works when logged in as the right role, and is blocked for other roles
- [ ] No secrets or personal data in the commit
