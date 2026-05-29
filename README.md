# DevPortfolio

Базовая структура портфолио на Django: проекты, навыки, опыт и главная страница.

## Быстрый старт

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/` для главной и `http://127.0.0.1:8000/admin/` для админки.

## Environment

Create `.env` from `.env.example` and set `DJANGO_SECRET_KEY`.

## Accounts lesson additions

- Added custom user model: `accounts.CustomUser`
- Added profile model with avatar resizing: `accounts.Profile`
- Added profile pages:
  - `http://127.0.0.1:8000/accounts/profile/`
  - `http://127.0.0.1:8000/accounts/profile/edit/`

> If you are switching an existing project from default Django user to a custom user model,
> start with a fresh database for this training project to avoid migration conflicts.
