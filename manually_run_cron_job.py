'''
Demonstrates using the Render API to start a cron job
outside of its defined schedule.

If you attempt to start a cron job while another run is
active, Render terminates the active run before starting
the new one.
'''
from auth import post_request

# Replace with your cron job's ID
CRON_JOB_ID = "cron-1a2b3c4d5e6f"

START_CRON_JOB_ENDPOINT_PATH = f"/cronjobs/{CRON_JOB_ID}/runs"

response = post_request(START_CRON_JOB_ENDPOINT_PATH)
