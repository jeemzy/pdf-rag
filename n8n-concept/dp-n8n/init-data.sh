#!/bin/bash
set -e

# This script runs only on first database initialization
# It creates a non-root user for n8n with limited privileges

if [ -n "$POSTGRES_NON_ROOT_USER" ] && [ -n "$POSTGRES_NON_ROOT_PASSWORD" ]; then
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER ${POSTGRES_NON_ROOT_USER} WITH PASSWORD '${POSTGRES_NON_ROOT_PASSWORD}';
        GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_NON_ROOT_USER};
        GRANT ALL ON SCHEMA public TO ${POSTGRES_NON_ROOT_USER};
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${POSTGRES_NON_ROOT_USER};
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${POSTGRES_NON_ROOT_USER};
EOSQL
    echo "Non-root user '${POSTGRES_NON_ROOT_USER}' created successfully"
else
    echo "POSTGRES_NON_ROOT_USER or POSTGRES_NON_ROOT_PASSWORD not set, skipping non-root user creation"
fi

