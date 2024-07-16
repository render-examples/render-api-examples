'''
Demonstrates using the Render API to scale a Render
background worker service up or down based on the current
size of a Redis job queue.

Render also provides built-in support for autoscaling,
based on a service's CPU and/or memory usage.
'''
from auth import get_request, post_request
import redis

# Define the base URL and the endpoints

# Replace with your worker service's ID
SERVICE_ID = "svc-a1b2c3d4e5f6"

# Replace with your Redis instance's ID
REDIS_ID = "rds-1a2b3c4d5e6f"

SCALE_ENDPOINT_PATH = f"/services/{SERVICE_ID}/scale"
REDIS_INFO_ENDPOINT_PATH = f"/redis/{REDIS_ID}/connection-info"

success, redis_connection_info = get_request(REDIS_INFO_ENDPOINT_PATH)
if not success:
    print("Failed to get Redis connection info")
    exit(1)

# Obtain Redis instance connection info
internal_connection_string = redis_connection_info.get('internalConnectionString')
r = redis.Redis.from_url(internal_connection_string)

# Get the current number of elements in the Redis queue
queue_length = r.llen('work_queue')
print(f"Number of elements in 'work_queue': {queue_length}")

# Calculate the number of instances to scale to based on
# the queue length (min 1, max 10)
instances_to_run = min(max(queue_length // 1000, 1), 10)
print(f"Instances to run based on queue length: {instances_to_run}")

scale_data = {
    "num_instances": instances_to_run
}
success, scale_response = post_request(SCALE_ENDPOINT_PATH, scale_data)
if success:
    print(f"Successfully scaled service {SERVICE_ID} to {instances_to_run} instances")
else:
    print(f"Failed to scale service {SERVICE_ID}")
