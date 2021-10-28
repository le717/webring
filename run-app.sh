#!/usr/bin/env bash
flask db migrate
rm .env
gunicorn --bind 0.0.0.0:80 --workers 2 --log-level error --access-logfile /app/log/access.log --error-logfile /app/log/error.log wsgi:app
