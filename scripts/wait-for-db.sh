#!/bin/bash
echo "Waiting for MySQL..."
MAX_RETRIES=30
COUNT=0
while ! mysqladmin ping -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
    echo "MySQL not ready ($COUNT/$MAX_RETRIES)"
    sleep 2
    COUNT=$((COUNT+1))
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo "Error: MySQL timeout."
        exit 1
    fi
done
echo "MySQL is up!"