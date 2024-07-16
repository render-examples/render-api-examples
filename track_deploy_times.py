'''
Demonstrates calculating recent deploy times for
each of your Render services.
'''
from auth import get_request
from datetime import datetime

SERVICES_ENDPOINT_PATH = "/services"
DEPLOYS_ENDPOINT_PATH = "/services/{service_id}/deploys"

success, services = get_request(SERVICES_ENDPOINT_PATH)
if not success:
    print("Failed to fetch services.")
    exit(1)

results = []

for service in services:
    service_id = service['service']['id']

    # Fetch one recent deploy for each service.
    # Increase the limit parameter if you want to adapt
    # this to calculate min/max/avg deploy times for
    # services.
    success, deploys = get_request(DEPLOYS_ENDPOINT_PATH.format(service_id=service_id), params={"limit": 1})

    if not success:
        print(f"Failed to fetch deploys for service {service_id}")
        continue

    deploy_time = deploys[0]['deploy']['createdAt']
    finished_time = deploys[0]['deploy']['finishedAt']

    # Convert from string to datetime objects
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

# Output a list of dictionaries with service_id,
# deploy_time, finished_time, and deployment_seconds for
# each service
print(results)
