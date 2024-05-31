```
## Airbyte API Client

Overview

A Python client for interacting with the Airbyte API. This client provides methods to update sources,
create connections, and delete connections, facilitating easy integration and management of data sync
processes within Airbyte.

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
    account_id="your_account_id",
    secret_key="your_secret_key",
    name="your_source_name"
)

# Example: Create a connection
api_client.create_connection(
    source_id="your_source_id",
    destination_id="your_destination_id",
    source_definition_id="your_source_definition_id",
    sync_mode="your_sync_mode",
    namespace_definition="your_namespace_definition",
    namespace_format="your_namespace_format",
    prefix="your_prefix",
    existing_connection_ids=["existing_connection_id1", "existing_connection_id2"]
)

# Example: Delete a connection
api_client.delete_connection(connection_id="your_connection_id")
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
