#!/bin/bash

set -e

# Setup environment
export APP_ROOT=/app

until nc -z -v -w30 $DB_HOST 5432
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

echo "Running migrate."
python src/manage.py migrate
echo "Finished migrate."

echo "Starting gunicorn"
gunicorn -c config/gunicorn/conf.py --bind :8000 --chdir src omdbapi.wsgi:application