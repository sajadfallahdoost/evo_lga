'''

-> venv ------------------

python -m venv .venv
source .venv/Scripts/activate
pip install numpy (example)
pip freeze > requirements.txt
poetry install

deactivate

-> postgres path ------------------

go to environment variable of your system
click on system env path and click on new
paste this: C:\Program Files\PostgreSQL\16\bin

for restore database:
python manage.py flush --noinput


-> set ssh-key ------------------

Check Existing Keys:
Get-Content $env:USERPROFILE\.ssh\id_rsa.pub

Generate SSH Key:
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

-> Redis ------------------

download redis

install(go to directory)
redis-server --service-install redis.windows.conf

start
redis-server --service-start

on setting
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Ensure this points to the correct Redis server
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CACHE_TTL = 300  # 5 minutes


redis-cli ping
redis-server --service-stop
redis-server --service-uninstall

on linux
sudo systemctl start redis-server
sudo systemctl status redis-server

-> Docker ------------------

docker-compose build
docker-compose up
docker-compose down

docker-compose ps
docker-compose build --no-cache


docker-compose up --build

we need 4 file(Dockerfile, docker-compose.yml, entrypoint.sh, .dockerignore):
----------
Dockerfile:
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.1

WORKDIR /code

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only the necessary files for installing dependencies
COPY pyproject.toml poetry.lock* /code/

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the rest of your application code
COPY . /code/

EXPOSE 8000

# Copy the entrypoint script into the container
COPY entrypoint.sh /code/entrypoint.sh

# Give execution rights on the entrypoint script
RUN chmod +x /code/entrypoint.sh

# Set the entrypoint script to be executed
ENTRYPOINT ["/code/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

----------
docker-compose.yml:
version: '3.11'
services:
  django:
    image: django-docker:0.0.1
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres
    environment:
      POSTGRES_DB: Backend
      POSTGRES_USER: Backend_user
      POSTGRES_PASSWORD: "sajadfallahdoost1234"

----------
entrypoint.sh:
#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser
echo "Creating superuser..."
python manage.py create_superuser

# Start Gunicorn server (if using Gunicorn, otherwise use runserver for development)
# gunicorn your_project_name.wsgi:application --bind 0.0.0.0:8000

# Start Django's development server (use for development only)
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
----------
.dockerignore:
__pycache__
db.sqlite3
.env

-> poetry ------------------
in powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
C:\Users\sajad\AppData\Roaming\Python\Scripts

poetry init
poetry install
poetry update
poetry add
poetry remove

poetry config --list
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "."

-> git ------------------

git config --global user.name "name"
git config --global user.email "your email"

git clone "repository code link"
git flow init
git remote add origin or git remote "repository code link"


git add . or git add "file name"
git commit -m 'commit message'  #first time use: git push origin develop
git push origin develop or main or master


git status

git remote -v
git log

git branch -a
git flow feature start sajad (for create new branch , you can write any name
for branch like develop, hotfix, ...)
git checkout "branch name"(main)

git merge "branch name"(main)

git reset
git fetch

git fetch origin

git reset --hard HEAD
git clean -fd


touch filename (for creating new file)

feat: A new feature
fix: A bug fix
chore: Routine tasks, maintenance, or refactoring
docs: Documentation updates
style: Code style changes (e.g., formatting)
test: Adding or modifying tests
perf: Performance-related changes
refactor: Code changes without adding features or fixing bugs
ci: Continuous Integration/Deployment configuration changes
----------
.gitignore:
# Created by https://www.gitignore.io

### OSX ###
.DS_Store
.AppleDouble
.LSOverride

# Icon must end with two \r
Icon

### Thumbnails ###
._*

# Files that might appear on the external disk
.Spotlight-V100
.Trashes

# Directories potentially created on remote AFP share
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk

### Python ###
### Byte-compiled / optimized / DLL files ###
__pycache__/
*.cpython-311
*.py[cod]
*.cpython-311
### C extensions ###
*.so

### Distribution / packaging ###
.Python
env/
.env
venv/
.venv
build/
develop-eggs/
dist/
downloads/
eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

### PyInstaller ###
# Usually, these files are written by a python script from a template
# Before PyInstaller builds the exe, to inject the date/other info into it
*.manifest
*.spec

### Installer logs ###
pip-log.txt
pip-delete-this-directory.txt

### Unit test / coverage reports ###
htmlcov/
.tox/
.coverage
.cache
nosetests.xml
coverage.xml

### Translations ###
*.mo
*.pot

### PyBuilder ###
target/

### Django ###
*.log
*.pyc
local_settings.py
collectstatic/
settings.ini
**/migrations/*
!**/migrations/__init__.py
media/upload/**
!media/upload/*
**/uploads/
**/upload/
.dccache

### Code editor ###
.vscode
.idea

### Database ###
db.sqlite3

### Docker ###
.dockerignore
entrypoint.sh
Dockerfile
docker-compose.yml

### Docs ###
!docs/**

### Sphinx documentation ###
docs/_build/

warehouse/tests/querysets/test_A.py
cache/
artifacts/
logs/

-> set DNS on ubuntu ------------------

sudo nano /etc/netplan/01-netcfg.yaml

network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
      nameservers:
        addresses:
          - 185.51.200.2
          - 178.22.122.100

sudo netplan apply


-> install Nekoray on ubuntu ------------------

sudo apt update && sudo apt upgrade -y
sudo apt install curl unzip -y
curl -L "https://github.com/nekoray/releases/download/v1.0/nekoray_v1.0_linux_amd64.zip" -o nekoray.zip
unzip nekoray.zip -d nekoray
chmod +x nekoray/nekoray
sudo mv nekoray/nekoray /usr/local/bin/
sudo nano /etc/nekoray/config.json
nekoray -c /etc/nekoray/config.json

-> How to start one Backend Django project from first  ------------------

git clone "repository code link"
git flow init
git push origin develop
poetry init
poetry config --list
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "."
poetry install
source .venv/Scripts/activate
poetry add django
django-admin startproject kernel .
poetry export -f requirements.txt > requirements.txt
python manage.py runserver
python manage.py startapp "your app name(like warehouse)"
django-admin startapp payment for inside app
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

change database to postgres:

psql -U postgres(in bash)

paste this text:

CREATE DATABASE "ecommerce" ;

CREATE USER "ecommerce_user" WITH PASSWORD 'Sf35741381@' ;

ALTER ROLE "ecommerce_user" SET client_encoding TO 'utf8' ;

ALTER ROLE "ecommerce_user" SET default_transaction_isolation TO 'read committed' ;

ALTER ROLE "ecommerce_user" SET timezone TO 'UTC' ;

ALTER USER "ecommerce_user" CREATEDB ;

GRANT ALL PRIVILEGES ON DATABASE ecommerce TO "ecommerce_user" ;

GRANT ALL ON schema public TO "ecommerce_user" ;

SELECT has_schema_privilege( 'ecommerce_user','public','CREATE') ;

ALTER DATABASE "ecommerce" OWNER TO "ecommerce_user" ;


change setting database to this :
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ecommerce",
        "USER": "ecommerce_user",
        "PASSWORD": "Sf35741381@",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "TEST": {"NAME": "ecommerce_test"},
    },
}

poetry add psycopg2

-> for deployment ------------------
first install poetry specific version:

sudo apt update
poetry self:uninstall
sudo apt install software-properties-common -y
sudo apt install python3.12 python3.12-venv python3.12-dev
sudo add-apt-repository ppa:deadsnakes/ppa
curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.3 python3 -
export PATH="$HOME/.local/bin:$PATH"
poetry env use python3.12

if get error on psycopg2 installing:
sudo apt install build-essential libpq-dev python3-dev
poetry add psycopg2-binary

ALLOWED_HOSTS = ["-", "127.0.0.1", "localhost"]
sudo apt update

poetry --version
poetry config --list
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "."

for postgres database:
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo -u postgres psql and paste this:
CREATE DATABASE "Backend";
CREATE USER "Backend_user" WITH PASSWORD 'sdjnnfejsajad3574nndfkd';
ALTER ROLE "Backend_user" SET client_encoding TO 'utf8';
ALTER ROLE "Backend_user" SET default_transaction_isolation TO 'read committed';
ALTER ROLE "Backend_user" SET timezone TO 'UTC';
ALTER USER "Backend_user" CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE Backend TO "Backend_user";
GRANT ALL ON schema public TO "Backend_user";
SELECT has_schema_privilege('Backend_user', 'public', 'CREATE');
ALTER DATABASE "Backend" OWNER TO "Backend_user";

nano setup_db.sql:
CREATE DATABASE "Backend";
CREATE USER "Backend_user" WITH PASSWORD 'sdjnnfejsajad3574nndfkd';
ALTER ROLE "Backend_user" SET client_encoding TO 'utf8';
ALTER ROLE "Backend_user" SET default_transaction_isolation TO 'read committed';
ALTER ROLE "Backend_user" SET timezone TO 'UTC';
ALTER USER "Backend_user" CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE "Backend" TO "Backend_user";
GRANT ALL ON schema public TO "Backend_user";
SELECT has_schema_privilege('Backend_user', 'public', 'CREATE');
ALTER DATABASE "Backend" OWNER TO "Backend_user";

psql -U postgres -f setup_db.sql
sudo -u postgres psql -f setup_db.sql

DROP DATABASE "Backend";
DROP USER "Backend_user";
REVOKE ALL PRIVILEGES ON SCHEMA public FROM "Backend_user";

\q

for redis database:
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
redis-cli ping

poetry install
python manage.py runserver 0.0.0.0:8000

'''

