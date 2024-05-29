# Airbyte API Client

A Python client for interacting with the Airbyte API. This client provides methods to update sources, create connections, and delete connections, facilitating easy integration and management of data sync processes within Airbyte.

## Installation

To install the Airbyte API client, you can use pip:

pip install airbyte-api-client


#USAGE

# Instantiate the API client
api_client = AirbyteApiClient("http://localhost:8000")

# Example: Update a source
api_client.update_source(source_id, account_id, secret_key, name)

# Example: Create a connection
api_client.create_connection(source_id, source_definition_id, destination_id, sync_mode, namespace_definition, namespace_format, prefix, existing_connection_ids)

# Example: Delete a connection
api_client.delete_connection(connection_id)

API Documentation
For more details on the Airbyte API, refer to the official documentation link below:
https://reference.airbyte.com/reference/start

Configuration
The Airbyte API client requires the base URL of your Airbyte instance. Make sure to initialize the client with the correct base URL.
