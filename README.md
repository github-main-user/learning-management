# Description
**The project is still in progress**.

A simple learning management system backend, powered by Django REST Framework.
On this moment this LMS system gives you an ability to manage your courses and lessons.
It implements auth using JWT system and uses stripe for payments

# Tech Stack
- Django 5.x
- Django REST Framework 3.x
- PostgreSQL
- Python 3.13+
- Celery(redis) + Celery beat
- Docker & Docker compose

# Quick Start

1. Clone the repo
```bash
git clone https://github.com/github-main-user/learning-management
```

2. Enter the cloned directory
```bash
cd learning-management
```

3. Set up the .env file
```bash
cp .env.example .env
```
Then open in your editor end setup

4. Start the project.
```bash
docker compose up --build
```

- `docker compose down -v` - to stop containers and remove volumes (`-v`).
- `docker compose logs` - to see all logs.
- `docker compose exec <db> <command>` - to execute a command on a started container.

- The application will be available on `http://localhost:8000/`
- Admin Panel on `http://localhost:8000/admin/`
