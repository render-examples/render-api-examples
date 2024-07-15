from auth import get_request
import json

success, payload = get_request('/services')
if not success:
  exit(1)

print('success!')
print(json.dumps(payload, indent=2, sort_keys=True))