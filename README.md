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
- API Documentation via Swagger/Redoc

# Quick Start
In case you want to try the project on your machine:

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

# Github Actions
In case you want to use automatic CICD via github actions:

1. Set up your server:
    - Install Docker
    - Set up firewall for 22(ssh) and 80(http) ports *(recommended but optional)*
    - Create a non-root user *(recommended but optional)*
2. Fork this repo
3. Setup github secrets:
    - `ENV_FILE` - file with all important variables *(see `.env.example` file)*.
    - `SERVER_IP` - IP address of your server.
    - `SSH_USER` - user name.
    - `SSH_SECRET_KEY` - *public* secret ssh key.

Every push/PR will trigger these github actions:
1. lint (flake8)
2. test
3. deploy

- The application will be available on `http://<SERVER_IP>:80/`
- Go to `api/docs` and `api/redoc` for documentation

To stop started application - `cd` to `/home/<SSH_USER>/learning-management/`,
and run `docker compose down` (add `-v` if you want to clear all volumes).
