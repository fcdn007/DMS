#!/usr/bin/env bash
python manage.py celery worker --loglevel=info -B
gunicorn databaseDemo.wsgi:application -c /home/wsl/mnt/f/wsl/project/databaseDemo2/gunicorn.conf.py
