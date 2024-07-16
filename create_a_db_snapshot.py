'''
Demonstrates using the Render API to start a create a database
snapshot and download it.
'''
from auth import post_request, get_request
import time
import requests
import urllib.parse

database_id = "db-1a2b3c4d5e6f"
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
            if backup["createdAt"] >= backup_timestamp:
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
