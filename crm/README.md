# CRM weekly Report Setup

This guide outlines the steps to set up and run the CRM application,including it scheduled tasks with Celery and Celery Beat

# Prerequisites

Before you begin, ensure that you have the following installed on you system

    - python 3.8+ and pip
    - Git
    -Redis

# Setup


1. Install Redis:
   sudo apt install redis-server
   sudo service redis start

2. Install dependencies:
   pip install -r requirements.txt

3. Run migrations:
   python manage.py migrate

4. Start Celery worker:
   celery -A crm worker -l info

5. Start Celery Beat:
   celery -A crm beat -l info

6. Verify logs:
   cat /tmp/crm_report_log.txt

# Setup Instructions

1. clone the Repository

```bash
git clone https://github.com/aabasimel/alx-backend-graphql_crm
cd alx-backend-graphql_crm
```
2. Install Redis and dependencies,Redis is required as the message broker for Celery
    - on macOS
    ```bash
    brew install redis
    brew services start redis
    ```
    - on Ubuntu/Debian
    ```bash
    sudo apt update
    sudo apt install redis-server
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    ```
3. Install python Dependencies: Install all required packages

```bash 
pip install -r requirements.txt
```
4. Run Database Migrations This will create the necessary database tables, including those for Celery Beat.
```bash 
python manage.py migrate
```

# Running the application
You need to run three separate processes in different terminal windows: the Django server, the Celery worker, and the Celery Beat scheduler.

1. Terminal 1: Run the Django Server (Optional, for development)
```bash 
python manage.py runserver
```
2. Terminal 2: Run the Celery Worker: The worker process executes the tasks.
```bash
celery -A crm worker -l info
```
3. Terminal 3: Run the Celery Beat Scheduler The scheduler (Beat) triggers tasks at their scheduled times.
```bash 
celery -A crm beat -l info
```

# Verify the report

The generate_crm_report task is scheduled to run every Monday at 6:00 AM (as per the schedule in settings.py).

To verify that it has run, you can check the log file:

```bash
cat /tmp/crm_report_log.txt
```





