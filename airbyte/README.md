```
## Airbyte API Client

Overview

A Python client for interacting with the Airbyte API. This client provides methods to update sources, create connections,
delete connections, list sources, and create sources, facilitating easy integration and management of data sync processes within Airbyte.


Installation
To install the Airbyte API client, you can use pip:

pip install airbyte-api-client

### Usage

Instantiate the API client:

```python
from airbyte_api_client import AirbyteApiClient

# Instantiate the API client
api_client = AirbyteApiClient("https://api.airbyte.com")


```python
# Example: Update a source
api_client.update_source(
    source_id="your_source_id",
)

# Example: Create a connection
api_client.create_connection(
    source_id="your_source_id",
    destination_id="your_destination_id"
)

# Example: Delete a connection
api_client.delete_connection(connection_id="your_connection_id")

# Example: List sources
sources = api_client.list_sources(limit=20, offset=0)
print(sources)

# Example: Create a source
response = api_client.create_source(
    name="your_source_name",
    workspace_id="your_workspace_id",
    configuration={"your_configuration_key": "your_configuration_value"}
)

```


## API Documentation

For more details on the Airbyte API, refer to the [official documentation](https://reference.airbyte.com/reference/start).

## Configuration

The Airbyte API client requires the base URL of your Airbyte instance. Make sure to initialize the client with the correct base URL.

## Changes

- Updated base URL and HTTP methods for endpoints to align with new API standards
- Updated `update_source` method to use PATCH instead of POST
- Modified `create_connection` method to handle payload as JSON string
- Updated `delete_connection` method to use DELETE instead of POST
- Improved error handling and exception raising
- Set default `base_url` to 'https://api.airbyte.com'
- Implemented keyword arguments for methods to allow optional parameters
- Added list_sources method to list sources
- Added create_source method to create a new source

## New Changes:

- Updated update_source method to accept **kwargs for additional parameters
- Updated create_connection method to accept **kwargs for additional parameters
- Simplified delete_connection by removing the explicit return type
- Changed list_sources to use requests.get instead of self.get
- Changed list_sources return type from dict to str
- Changed create_source to use requests.post instead of self.post

