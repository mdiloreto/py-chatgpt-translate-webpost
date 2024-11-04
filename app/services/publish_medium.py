import requests
from requests.exceptions import RequestException, HTTPError, JSONDecodeError

class MediumPublisher:
    def __init__(self, access_token):
        self.base_url = "https://api.medium.com/v1"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def create_post(self, user_id, title, content):
        url = f"{self.base_url}/users/{user_id}/posts"
        data = {
            "title": title,
            "contentFormat": "markdown",
            "content": content,
            "tags": [],
            "publishStatus": "draft"
        }
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            return response.json()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(response.text)
        except JSONDecodeError as json_err:
            print(f"JSON decode error: {json_err}")
            print(response.text)
        except RequestException as req_err:
            print(f"Request failed: {req_err}")


    def get_user_id(self):
        url = f"{self.base_url}/me"
        response = requests.get(url, headers=self.headers)
        try:
            if response.status_code == 200:
                return response.json().get("data").get("id")
            else:
                # Handle non-OK responses
                print(f"Error: Received status code {response.status_code}")
                print(f"Response body: {response.text}")
                return None
        except requests.exceptions.JSONDecodeError as e:
            # Handle JSON decode error
            print(f"JSONDecodeError: {e}")
            print(f"Response body: {response.text}")
            return None
