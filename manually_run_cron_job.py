'''
Render cron jobs are scheduled to start at a specific time, but what if you want to start a cron job manually?

This example shows you how to start a cron job manually using the Render API.

Note that Render only allows one copy of a cron job to run, to avoid problems with parallel execution. You can use the `force` parameter to force start the cron job, which will stop the currently running job and start a new one.

Any cron jobs that are terminated will be sent a SIGTERM signal, and will have about 30 seconds to shut down before being forcibly terminated.

'''
from auth import post_request

cron_job_id = "cron-1a2b3c4d5e6f"
start_cron_job_endpoint = f"/cronjobs/{cron_job_id}/runs"

# you could add some conditional checking here to know whether to start the cron job or not

response = post_request(start_cron_job_endpoint)
