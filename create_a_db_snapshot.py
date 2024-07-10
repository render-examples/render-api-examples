'''
Render provides a [database snapshot once per day](https://docs.render.com/postgresql-backups) for your managed databases, but you can use the API to create your own snapshots whenever you like. This can be useful for creating backups before making changes to your database schema, or for creating a snapshot before running a large migration.

This example shows you how to create a snapshot of a Render managed database using the Render API.

The `pg_dump` utility cannot take a password parameter. You will need to set up a `.pgpass` file to handle the authentication. You can read more about this in the PostgreSQL documentation at https://www.postgresql.org/docs/current/libpq-pgpass.html
(This .pgpass file is only used to match the password with other details like hostname, username, and database name used below)

'''
from auth import post_request

database_id = "db-1a2b3c4d5e6f"
suspend_endpoint = f"/databases/{database_id}/suspend"
restart_endpoint = f"/databases/{database_id}/restart"

# Suspend the database
suspend_response = post_request(suspend_endpoint)
if not suspend_response:
    print("Failed to suspend the database.")
    exit(1)

# Run pg_dump in the background
import subprocess

DB_USERNAME = os.getenv("DB_USERNAME")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_DATABASE = os.getenv("DB_DATABASE")

try:
    subprocess.run([
        "pg_dump", 
        "-U", DB_USERNAME, 
        "-h", DB_HOSTNAME,
        DB_DATABASE
    ], check=True, stdout=open("backup.sql", "w"))

    print("Database backup created successfully.")
except subprocess.CalledProcessError as e:
    print(f"Failed to create database backup: {e}")
finally:
    # handle any other cleanup here that you might need
    pass

# Resume the database
restart_response = post_request(restart_endpoint)
if restart_response:
    print("Database restarted successfully:")
    print(restart_response)
else:
    print("Failed to restart the database.")
