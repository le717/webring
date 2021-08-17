#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:80 --workers 2 --log-level error --access-logfile /app/log/webring.access.log --error-logfile /app/log/webring.error.log wsgi:app
