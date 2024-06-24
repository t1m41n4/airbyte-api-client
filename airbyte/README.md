```
## Airbyte API Client

Overview

A Python client for interacting with the Airbyte API. This client provides methods to update sources,
create connections, delete connections, list sources, and create sources, facilitating easy
integration and management of data sync processes within Airbyte.


Installation
To install the Airbyte API client, you can use pip:

pip install airbyte-api-client

### Usage

Instantiate the API client:

```python
from airbyte_api_client import AirbyteApiClient
api_client = AirbyteApiClient("https://api.airbyte.com/v1")


```python
# Example: Update a source with additional parameters
api_client.update_source(
    source_id="your_source_id",
    name="updated_source_name",
    workspace_id="your_workspace_id",
    connectionConfiguration={"your_new_configuration_key": "your_new_configuration_value"}
)

# Example: Create a connection with additional parameters
api_client.update_source(
    source_id="your_source_id",
    name="updated_source_name",
    workspace_id="your_workspace_id",
    connectionConfiguration={"your_new_configuration_key": "your_new_configuration_value"}
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
    sourceDefinitionId="your_source_definition_id",
    connectionConfiguration={"your_configuration_key": "your_configuration_value"}
)

```


## API Documentation

For more details on the Airbyte API, refer to the [official documentation](https://reference.airbyte.com/reference/).

## Configuration

The Airbyte API client requires the base URL of your Airbyte instance. Initialize the client with the correct base URL and optionally configure other parameters using environment variables or directly in your code.

## Changes

- Updated base URL and HTTP methods for endpoints to align with new API standards.
- Enhanced `update_source` method to support additional parameters using **kwargs.
- Improved `create_connection` method to handle JSON payload more efficiently.
- Simplified `delete_connection` method by removing explicit return type.
- Optimized `list_sources` method to use `requests.get` directly for improved performance.
- Refactored `create_source` method to use `requests.post` for clearer code structure and consistency.
- Improved error handling and response messaging throughout the API client.
- Added support for environment variables to configure API client parameters.
- Implemented HTTP Basic Authentication for secure API requests.
- Set default `base_url` to 'https://api.airbyte.com/v1'

