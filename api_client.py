import requests
from requests.exceptions import RequestException
import json
from urllib.parse import urljoin
import os
import logging
from enum import Enum

# Set up logging with a more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HTTPMethod(Enum):
    """HTTP methods supported by the client"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class APIError(Exception):
    """Custom exception for API-related errors"""
    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)
        # Log the error when it's created
        logger.error(f"API Error: {message} (Status: {status_code})")


class APIClient:
    """
    API Client for making requests to the API
    Args:
        base_url: Base URL for the API. If not provided, will be read from environment variable.
        api_key: Optional API key for authentication
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates
        default_headers: Default headers to include in all requests

    Examples:
        client = APIClient(base_url='https://api.app.com/v1')
        client.get('/users')
        client.post('/users', data={'name': 'John Doe'})
        client.put('/users/1', data={'name': 'Jane Doe'})
        client.delete('/users/1')
    """
    DEFAULT_BASE_URL_ENV = 'API_BASE_URL'

    def __init__(
        self,
        base_url=None,
        api_key=None,
        timeout=30,
        verify_ssl=True,
        default_headers=None
    ):
        logger.info("Initializing API client")
        self.base_url = self._get_base_url(base_url)
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if default_headers:
            self.default_headers.update(default_headers)
        if api_key:
            self.default_headers['Authorization'] = f'Bearer {api_key}'
        
        self.session.headers.update(self.default_headers)
        logger.info(f"API client initialized with base URL: {self.base_url}")

    def _get_base_url(self, base_url):
        """Get base URL from parameter or environment variable."""
        if base_url is not None:
            return base_url.rstrip('/')
        
        env_base_url = os.getenv(self.DEFAULT_BASE_URL_ENV)
        if env_base_url is None:
            error_msg = f"Base URL must be provided either directly or through environment variable '{self.DEFAULT_BASE_URL_ENV}'"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return env_base_url.rstrip('/')

    def _build_url(self, endpoint):
        """Build full URL from endpoint."""
        return urljoin(f"{self.base_url}/", endpoint.lstrip('/'))

    def _handle_response(self, response):
        """Handle API response and raise appropriate exceptions."""
        try:
            response.raise_for_status()
            if response.headers.get('content-type', '').startswith('application/json'):
                return response.json()
            return response.text
                
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            raise APIError(
                message=f"HTTP error occurred: {str(e)}",
                status_code=response.status_code,
                response=response
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {str(e)}")
            raise APIError(
                message=f"Failed to decode JSON response: {str(e)}",
                status_code=response.status_code,
                response=response
            )
        except RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise APIError(f"Request failed: {str(e)}")

    def _log_request(self, method, url):
        """Log request details"""
        logger.info(f"Making {method} request to {url}")

    def get(self, endpoint, params=None, **kwargs):
        """Send GET request to the API."""
        url = self._build_url(endpoint)
        self._log_request('GET', url)
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            return self._handle_response(response)
        except RequestException as e:
            logger.error(f"GET request to {url} failed: {str(e)}")
            raise APIError(f"GET request failed: {str(e)}")

    def post(self, endpoint, data=None, json_data=None, **kwargs):
        """Send POST request to the API."""
        url = self._build_url(endpoint)
        self._log_request('POST', url)
        try:
            response = self.session.post(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            return self._handle_response(response)
        except RequestException as e:
            logger.error(f"POST request to {url} failed: {str(e)}")
            raise APIError(f"POST request failed: {str(e)}")

    def put(self, endpoint, data=None, json_data=None, **kwargs):
        """Send PUT request to the API."""
        url = self._build_url(endpoint)
        self._log_request('PUT', url)
        try:
            response = self.session.put(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            return self._handle_response(response)
        except RequestException as e:
            logger.error(f"PUT request to {url} failed: {str(e)}")
            raise APIError(f"PUT request failed: {str(e)}")

    def delete(self, endpoint, **kwargs):
        """Send DELETE request to the API."""
        url = self._build_url(endpoint)
        self._log_request('DELETE', url)
        try:
            response = self.session.delete(
                url,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            return self._handle_response(response)
        except RequestException as e:
            logger.error(f"DELETE request to {url} failed: {str(e)}")
            raise APIError(f"DELETE request failed: {str(e)}")

    def patch(self, endpoint, data=None, json_data=None, **kwargs):
        """Send PATCH request to the API."""
        url = self._build_url(endpoint)
        self._log_request('PATCH', url)
        try:
            response = self.session.patch(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            return self._handle_response(response)
        except RequestException as e:
            logger.error(f"PATCH request to {url} failed: {str(e)}")
            raise APIError(f"PATCH request failed: {str(e)}")

    def close(self):
        """Close the session and cleanup resources."""
        logger.info("Closing API client session")
        self.session.close()
