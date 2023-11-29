#!/bin/sh

echo "Waiting for Postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

python3 src/manage.py makemigrations
python3 src/manage.py migrate

exec "$@"
