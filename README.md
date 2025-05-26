# Python API Client

A robust and easy-to-use HTTP client for making requests to REST APIs. This client provides a simple interface for making HTTP requests with built-in error handling, logging, and support for environment-based configuration.

## Features

- Simple and intuitive API
- Automatic JSON handling
- Environment variable support for configuration
- Comprehensive error handling
- Request logging
- Session management
- Support for all HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Query parameter support
- JSON and form data support
- Custom headers support
- API key authentication

## Usage

### Basic Usage

```python
from api_client import APIClient

client = APIClient(
    base_url="https://api.example.com",
    api_key="your-api-key-here"
)

users = client.get("users", params={"page": 1, "limit": 10})
new_user = client.post("users", json_data={"name": "John Doe"})

client.close()
```
