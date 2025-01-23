import requests
from requests.auth import HTTPBasicAuth

class ApiClient:
    """API client class to make requests to a REST API"""
    def __init__(self, base_url, username, password, api_key):
        """Inits the ApiClient with the API key, base URL and credentials"""
        self.api_key = api_key
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)

    def get(self, endpoint, params=None):
        """Makes a GET request to the API"""
        url = f"{self.base_url}/{endpoint}/{self.api_key}"
        try:
            response = requests.get(url, params=params, auth=self.auth, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

  


