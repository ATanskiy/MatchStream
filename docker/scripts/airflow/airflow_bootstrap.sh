#!/bin/bash
set -e

echo "🔍 Checking Airflow metadata DB state..."

# Check if migrations table exists → DB initialized
if airflow db check-migrations > /dev/null 2>&1; then
    echo "✅ Airflow DB already initialized"
else
    echo "⚠️ DB not initialized → running airflow db init"
    airflow db init
fi

echo "🔍 Checking if admin user exists..."

# Check if admin user exists
if airflow users list --output table | grep -w "admin" > /dev/null 2>&1; then
    echo "✅ Admin user already exists"
else
    echo "⚠️ Admin user missing → creating..."
    airflow users create \
        --username admin \
        --password admin \
        --firstname admin \
        --lastname admin \
        --role Admin \
        --email admin@example.com
fi

echo "🚀 Starting Airflow Webserver..."
exec airflow webserver
