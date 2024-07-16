'''
Demonstrates using the Render API to create a database
backup and download it.
'''
from auth import post_request, get_request
import time
import requests
import urllib.parse

# Replace with your database's ID
DATABASE_ID = "db-1a2b3c4d5e6f"

BACKUP_ENDPOINT_PATH = f"/postgres/{DATABASE_ID}/backup"

# Get the current date/time without seconds in UTC
backup_timestamp = time.strftime("%Y-%m-%dT%H:%M:00Z", time.gmtime())
print(backup_timestamp)

# Start a backup
success, payload = post_request(BACKUP_ENDPOINT_PATH)
if not success:
    print("Failed to initiate database backup.")
    exit(1)

WAIT_TIME_SECONDS = 30
backup_url = ''
done = False

# Every 30 seconds, fetch recent backups until we
# observe a backup captured after backup_timestamp
while not done:
    success, payload = get_request(BACKUP_ENDPOINT_PATH)
    print(payload)
    if success:
        for backup in payload:
            if backup["createdAt"] >= backup_timestamp:
                backup_url = backup["url"]
                done = True
                break
            else:
                print(f'{backup["createdAt"]} precedes {backup_timestamp}')
    time.sleep(WAIT_TIME_SECONDS)

# Fetch the backup from its URL
filename = urllib.parse.urlparse(backup_url).path.split("/")[-1]
r = requests.get(backup_url)
if r.status_code == 200:
    with open(filename, "wb") as f:
        f.write(r.content)
    print("Backup created successfully.")
