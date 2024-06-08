#!/usr/bin/env bash
# Run database migrations
python ./scripts/make_database.py
flask db migrate
flask db seed
rm .env

# Start the application
gunicorn --bind 0.0.0.0:80 --workers 2 --log-level error --access-logfile /app/log/access.log --error-logfile /app/log/error.log wsgi:app
