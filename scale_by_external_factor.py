'''
Render can scale your services based on CPU, memory, or bandwidth.

What if you want to scale your services up or down based on other external factors?

This example will show you how to scale a service worker based on a queue count from Redis. We'll keep one worker running for every 1,000 jobs in the queue, with a minimum of 1 and maximum of 10.
'''
from auth import get_request, post_request
import redis

# Define the base URL and the endpoints
service_id = "svc-a1b2c3d4e5f6"   # your real worker service ID would go here
redis_id = "rds-1a2b3c4d5e6f"     # your real Redis instance ID would go here

service_endpoint = f"/services/{service_id}"
scale_endpoint = f"/services/{service_id}/scale"
redis_connection_info_endpoint = f"/redis/{redis_id}/connection-info"

success, redis_connection_info = get_request(redis_connection_info_endpoint)
if not success:
    print("Failed to get Redis connection info")
    exit(1)

# Connect to Redis
internal_connection_string = redis_connection_info.get('internalConnectionString')
r = redis.Redis.from_url(internal_connection_string)

queue_length = r.llen('work_queue')
print(f"Number of elements in 'work_queue': {queue_length}")

instances_to_run = min(max(queue_length // 1000, 1), 10)
print(f"Instances to run based on queue length: {instances_to_run}")

scale_data = {
    "num_instances": instances_to_run
}
success, scale_response = post_request(scale_endpoint, scale_data)
if success:
    print(f"Successfully scaled service {service_id} to {instances_to_run} instances")
else:
    print(f"Failed to scale service {service_id}")
