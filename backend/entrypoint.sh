#!/bin/bash

until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_DB -c 'SELECT 1' &> /dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing command"

# Start Messages forwarder service
python services/messages_forwarder.py &
# Start main service
exec "$@"