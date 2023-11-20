#!/bin/bash

check_postgres() {
    until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_DB -q -t 1; do
        >&2 echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    >&2 echo "PostgreSQL is up - continuing"
}

check_postgres

# Start Messages forwarder service
python services/messages_forwarder.py &
# Start main service
exec "$@"