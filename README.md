# 🎯 TalentScout

TalentScout is a job recruitment platform built with Django, Django Channels, and integrated with OAuth (Google and GitHub) using `django-allauth`. It supports real-time messaging, employer-only access control, and PostgreSQL for production.

---

## 🚀 Features

- Employer & job seeker authentication
- OAuth login via Google and GitHub
- Employer-only middleware
- Job posting and management
- Real-time messaging using Django Channels & Redis
- Celery integration for background tasks
- RESTful architecture (optional: if using DRF)
- Render deployment-ready

---

## 🏗️ Tech Stack

- **Backend**: Django
- **Auth**: django-allauth (email + social login)
- **Real-Time**: Django Channels + Redis
- **Background Jobs**: Celery + Redis
- **Database**: PostgreSQL (production), SQLite (development)
- **Deployment**: Render
- **Frontend**: Django templates (or plug in React/Vue separately)

---

## 🧾 Project Structure

talentscout/
├── manage.py
├── .env
├── requirements.txt
├── users/
├── employers/
├── jobs/
├── messaging/
├── talentscout/ # core project folder (settings, wsgi, asgi)
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── static/
└── templates/

yaml
Copy
Edit

---

## ⚙️ Environment Setup

1. **Clone the project**

bash
git clone https://github.com/yourusername/talentscout.git
cd talentscout
Create & activate a virtual environment

bash
Copy
Edit
python -m venv .venv
.venv\Scripts\activate  # Windows
# OR
source .venv/bin/activate  # Unix/macOS
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Create .env file

env
Copy
Edit
# .env

SECRET_KEY=your-secret-key
DEBUG=True

# PostgreSQL for Render or local dev
DATABASE_URL=postgres://user:password@localhost:5432/yourdb

# Redis
REDIS_URL=redis://localhost:6379

# Social Auth
SOCIAL_AUTH_GOOGLE_CLIENT_ID=xxx
SOCIAL_AUTH_GOOGLE_SECRET=xxx

SOCIAL_AUTH_GITHUB_CLIENT_ID=xxx
SOCIAL_AUTH_GITHUB_SECRET=xxx
Run migrations & start the server

bash
Copy
Edit
python manage.py migrate
python manage.py runserver
🛰️ Deployment on Render
Set Root Directory to talentscout/talentscout

Set Build Command:

bash
Copy
Edit
pip install -r requirements.txt
Set Start Command:

bash
Copy
Edit
gunicorn talentscout.wsgi:application
Add environment variables from .env in Render dashboard

🧪 Tests
bash
Copy
Edit
python manage.py test
✨ TODOs / Improvements
 Add unit tests

 Add CI/CD pipeline (GitHub Actions or Render auto-deploy)

 REST API (via Django REST Framework)

 Frontend integration (React/Vue)

 Notification system (via WebSocket or Celery)

