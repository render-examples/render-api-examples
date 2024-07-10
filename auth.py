import os
import requests

# We recommend setting your API token as an environment variable for better security
api_token = os.getenv("RENDER_API_TOKEN")

# render's API base URL
base_url = "https://api.render.com/v1"

# set a dictionary/map for any headers to send, which mush include the Authorization header with your bearer token and setting the content type to be JSON
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# methods to do GET/POST requests to the Render API, we'll use these in other examples below
def get_request(endpoint, params=None):
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return True, response.json()
    else:
        print(f"Failed to fetch data from {endpoint} with status code: {response.status_code}")
        print(response.text)
        return False, None

def post_request(endpoint, data):
    response = requests.post(base_url + endpoint, headers=headers, json=data)
    if response.status_code in [200, 201]:
        return True, response.json()
    else:
        print(f"Failed to post data to {endpoint} with status code: {response.status_code}")
        print(response.text)
        return False, None
