'''
A customer of Render tweeted about how they wanted to track the deploy times of their services on Render.

To accomplish this, their script would need to do the following:
- get a list of all services
- call the deploy endpoint for each service to get the deploy times
- calculate the latest deploy time for each service

'''

from auth import get_request
from datetime import datetime

services_endpoint = "/services"
deploys_endpoint = "/services/{service_id}/deploys"

success, services = get_request(services_endpoint)
if not success:
    print("Failed to fetch services.")
    exit(1)

results = []

for service in services:
    service_id = service['service']['id']

    # remove the limit if you want to grab all deployment times to calculate min/max/avg
    success, deploys = get_request(deploys_endpoint.format(service_id=service_id), params={"limit": 1})
    
    if not success:
        print(f"Failed to fetch deploys for service {service_id}")
        continue

    deploy_time = deploys[0]['deploy']['createdAt']
    finished_time = deploys[0]['deploy']['finishedAt']
    
    # convert from string to datetime objects
    dt_deploy_time = datetime.strptime(deploy_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt_finished_time = datetime.strptime(finished_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    diff_seconds = (dt_finished_time - dt_deploy_time).total_seconds()

    results.append({
        "service_id": service_id,
        "service_name": service['service']['name'],
        "deploy_time": deploy_time,
        "finished_time": finished_time,
        "deployment_seconds": diff_seconds
    })

print(results)
# Expected output: a list of dictionaries with service_id, deploy_time, finished_time, and total_time for each service
