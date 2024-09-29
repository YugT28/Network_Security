#!/bin/bash

# Initialize Airflow database if not already done
airflow db init

# Create Airflow user (admin)
airflow users create -e sunnythakare8@gmail.com -f sunny -p admin -r Admin -u admin

# Run the main process
exec "$@"
