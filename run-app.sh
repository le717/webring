#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:80 --workers 2 --log-level error --access-logfile /var/log/gunicorn.access.log --error-logfile /var/log/gunicorn.error.log wsgi:app
