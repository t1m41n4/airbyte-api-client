"""
API Client for interacting with Airbyte, a data integration platform.
This client provides methods to update sources, create connections,
and delete connections within an Airbyte instance.
"""

import requests

from requests import Response
import json


class AirbyteApiClient:
    """Airbyte API Client."""

    def __init__(self, base_url: str = "https://api.airbyte.com") -> None:
        """Initialize the Airbyte API Client."""
        self.base_url = base_url

    def update_source(self, source_id, account_id=None, secret_key=None, name=None) -> Response:
        """Update a source in the Airbyte API."""
        url = f"{self.base_url}/v1/sources/{source_id}"
        headers = {"Content-Type": "application/json"}
        data = {
            "sourceId": source_id,
            "name": name,
            "connectionConfiguration": {
                "account_id": account_id,
                "api_key": secret_key,
            },
        }
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            print(
                f"Source {source_id} updated successfully with account ID: {account_id}"
            )
        else:
            raise Exception(f"Failed to update source {source_id}: {response.content}")

        return response

    def create_connection(
        self,
        source_id,
        destination_id,
        source_definition_id=None,
        sync_mode=None,
        namespace_definition=None,
        namespace_format=None,
        prefix=None,
        existing_connection_ids=None,
    ) -> str:
        """Create a new connection in the Airbyte API."""
        url = f"{self.base_url}/v1/connections"
        headers = {"Content-Type": "application/json"}
        payload = {
            "sourceId": source_id,
            "destinationId": destination_id,
            "sourceDefinitionId": source_definition_id,
            "syncMode": sync_mode,
            "namespaceDefinition": namespace_definition,
            "namespaceFormat": namespace_format,
            "prefix": prefix,
            "existingConnectionIds": existing_connection_ids,
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            connection_data = response.json()
            connection_id = connection_data["connectionId"]
            print("Connection created successfully")
        else:
            raise Exception(f"Failed to create connection: {response.content}")

        return str(connection_id)

    def delete_connection(self, connection_id) -> None:
        """Delete a connection in the Airbyte API."""
        url = f"{self.base_url}/v1/connections/{connection_id}"
        response = requests.delete(url)
        if response.status_code == 200:
            print(f"Connection {connection_id} deleted successfully")
        else:
            raise Exception(
                f"Failed to delete connection {connection_id}: {response.content}"
            )

    def list_sources(self, limit: int = 20, offset: int = 0) -> dict:
        """List sources in the Airbyte API."""
        url = f"{self.base_url}/v1/sources"
        params = {"includeDeleted": False, "limit": limit, "offset": offset}
        response = self.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to list sources: {response.content}")

    def create_source(
        self, name, workspace_id, configuration, definition_id=None
    ) -> Response:
        """Create a new source in the Airbyte API."""
        url = f"{self.base_url}/v1/sources"
        payload = {
            "name": name,
            "workspaceId": workspace_id,
            "configuration": configuration,
            "definitionId": definition_id,
        }
        response = self.post(url, json=payload)
        if response.status_code == 200:
            print("Source created successfully")
        else:
            raise Exception(f"Failed to create source: {response.content}")

        return response
