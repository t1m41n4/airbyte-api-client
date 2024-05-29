"""
API Client for interacting with Airbyte, a data integration platform.
This client provides methods to update sources, create connections,
and delete connections within an Airbyte instance.
"""

import requests
import json


class AirbyteApiClient:
    """Airbyte API Client."""

    def __init__(self, base_url):
        """Initialize the Airbyte API Client."""
        self.base_url = base_url

    def update_source(self, source_id, account_id, secret_key, name):
        """Update a source in the Airbyte API."""
        url = f"{self.base_url}/api/v1/sources/update"
        headers = {"Content-Type": "application/json"}
        data = {
            "sourceId": source_id,
            "name": name,
            "connectionConfiguration": {
                "account_id": account_id,
                "api_key": secret_key,
            },
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print(
                f"Source {source_id} updated successfully with account ID: {account_id}"
            )
            return response.json()
        else:
            print(f"Failed to update source {source_id}: {response.content}")
            return None

    def create_connection(
        self,
        source_id,
        source_definition_id,
        destination_id,
        sync_mode,
        namespace_definition,
        namespace_format,
        prefix,
        existing_connection_ids,
    ):
        """Create a new connection in the Airbyte API."""
        url = f"{self.base_url}/api/v1/connections/create"
        headers = {"Content-Type": "application/json"}
        data = {
            "sourceId": source_id,
            "sourceDefinitionId": source_definition_id,
            "destinationId": destination_id,
            "syncMode": sync_mode,
            "namespaceDefinition": namespace_definition,
            "namespaceFormat": namespace_format,
            "prefix": prefix,
            "existingConnectionIds": existing_connection_ids,
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            connection_data = response.json()
            connection_id = connection_data["connectionId"]
            print("Connection created successfully")
            return connection_id
        else:
            print(f"Failed to create connection: {response.content}")
            return None

    def delete_connection(self, connection_id):
        """Delete a connection in the Airbyte API."""
        url = f"{self.base_url}/api/v1/connections/delete"
        headers = {"Content-Type": "application/json"}
        data = {"connectionId": connection_id}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"Connection {connection_id} deleted successfully")
        else:
            print(f"Failed to delete connection {connection_id}: {response.content}")
