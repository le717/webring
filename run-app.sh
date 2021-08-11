#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:80 --workers 2 --log-level error --access-logfile /app/log/gunicorn.access.log --error-logfile /app/log/gunicorn.error.log wsgi:app
