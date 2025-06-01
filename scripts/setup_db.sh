#!/bin/bash
# Script to set up the database for the Language School Management System

# Load environment variables from .env file
if [ -f ../.env ]; then
    export $(grep -v '^#' ../.env | xargs)
else
    echo "Error: .env file not found. Please create it from .env.example."
    exit 1
fi

# Check if MySQL client is installed
if ! command -v mysql &> /dev/null; then
    echo "Error: MySQL client not found. Please install it."
    exit 1
fi

# Create the database if it doesn't exist
echo "Creating database ${DB_NAME} if it doesn't exist..."
mysql -h ${DB_HOST} -P ${DB_PORT} -u ${DB_USER} -p${DB_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Check if the database was created successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to create database. Please check your MySQL credentials."
    exit 1
fi

# Import the database schema
echo "Importing database schema..."
mysql -h ${DB_HOST} -P ${DB_PORT} -u ${DB_USER} -p${DB_PASSWORD} ${DB_NAME} < ../database/init.sql

# Check if the schema was imported successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to import database schema. Please check the init.sql file."
    exit 1
fi

echo "Database setup complete!"
echo "You can now run the application with 'python main.py'"