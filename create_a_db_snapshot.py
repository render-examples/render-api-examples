'''
Render provides a [database snapshot once per day](https://docs.render.com/postgresql-backups) for your managed databases, but you can use the API to create your own snapshots whenever you like. This can be useful for creating backups before making changes to your database schema, or for creating a snapshot before running a large migration.

This example shows you how to create a snapshot of a Render managed database using the Render API.

The `pg_dump` utility cannot take a password parameter. You will need to set up a `.pgpass` file to handle the authentication. You can read more about this in the PostgreSQL documentation at https://www.postgresql.org/docs/current/libpq-pgpass.html
(This .pgpass file is only used to match the password with other details like hostname, username, and database name used below)

'''
from auth import post_request, get_request
import time
import requests
import urllib.parse

database_id = "db-1a2b3c4d5e6f"
database_id = 'dpg-cqaq8mt6l47c73cl96s0-a'
backup_endpoint = f"/postgres/{database_id}/backup"

# get the current date/time without seconds in UTC
backup_timestamp = time.strftime("%Y-%m-%dT%H:%M:00Z", time.gmtime())
print(backup_timestamp)

# start a backup
success, payload = post_request(backup_endpoint)
if not success:
    print("Failed to back up the database.")
    exit(1)

wait_time = 30
backup_url = ''
done = False
while not done:
    # fetch the backup endpoint until we see our backup_timestamp in the createdAt field in the results
    success, payload = get_request(backup_endpoint)
    print(payload)
    if success:
        for backup in payload:
            if backup["createdAt"] == backup_timestamp:
                backup_url = backup["url"]
                done = True
                break
            else:
                print(f'{backup["createdAt"]} != {backup_timestamp}')
    time.sleep(wait_time)

# fetch the backup URL
filename = urllib.parse.urlparse(backup_url).path.split("/")[-1]
r = requests.get(backup_url)
if r.status_code == 200:
    with open(filename, "wb") as f:
        f.write(r.content)
    print("Backup created successfully.")
