# How we work together

## 1. Work on a branch, never directly on `main`

```bash
git checkout main
git pull                                  # get everyone's latest work
git checkout -b feature/logbook-entries   # one branch per task
# ...make your changes...
git add .
git commit -m "Add logbook entry form"
git push -u origin feature/logbook-entries
```

Then open a **pull request** on GitHub so another team member can check it before it is merged into `main`.

## 2. Stay in your own app

Only change files in your own app (`apps/<your_app>/`). If you need to change `config/settings.py`, `config/urls.py`, `templates/base.html` or another person's app, tell the group first. These shared files are where merge conflicts happen.

## 3. Migrations

- After changing `models.py`, run `python manage.py makemigrations <your_app>` and commit the new migration file together with the model change.
- Never edit or delete a migration that is already on `main`. Make a new one instead.
- After pulling `main`, always run `python manage.py migrate`.

## 4. Before you open a pull request

```bash
git checkout main && git pull
git checkout feature/your-branch && git merge main
python manage.py migrate
python manage.py test
```

Never commit `.env`, `db.sqlite3` or uploaded files. `.gitignore` already blocks them.
