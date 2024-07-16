# Demonstrates authenticating with the Render API
# using a bearer token. Other examples in this repo
# import this module to authenticate with the Render API.
import os
import requests

# For security, set your API key as an environment variable
# instead of hardcoding it.
API_KEY = os.getenv("RENDER_API_KEY")

# The Render API's base URL
API_BASE_URL = "https://api.render.com/v1"

# Define a dictionary of headers to include in every
# request. Must include an Authorization header with your
# bearer token and setting the content type to JSON
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Methods for sending GET/POST requests to the Render API
def get_request(endpoint, params=None):
    response = requests.get(API_BASE_URL + endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return True, response.json()
    else:
        print(f"Failed to fetch data from {endpoint} with status code: {response.status_code}")
        print(response.text)
        return False, None

def post_request(endpoint, data):
    response = requests.post(API_BASE_URL + endpoint, headers=headers, json=data)
    if response.status_code in [200, 201, 202]:
        if response.text:
            return True, response.json()
        else:
            return True, None
    else:
        print(f"Failed to post data to {endpoint} with status code: {response.status_code}")
        print(response.text)
        return False, None
