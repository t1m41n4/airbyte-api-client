"""
API Client for interacting with Airbyte, a data integration platform.
This client provides methods to update sources, create connections,
delete connections, list sources, and create sources within an Airbyte instance.
"""

import requests

import json


class AirbyteApiClient:
    """Airbyte API Client."""

    def __init__(self, base_url: str = "https://api.airbyte.com") -> None:
        """Initialize the Airbyte API Client."""
        self.base_url = base_url

    def update_source(self, source_id, **kwargs) -> None:
        """Update a source in the Airbyte API."""
        url = f"{self.base_url}/v1/sources/{source_id}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "sourceId": source_id,
        }
        payload.update(kwargs)
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(
                f"Source {source_id} updated successfully"
            )
        else:
            raise Exception(f"Failed to update source {source_id}: {response.content}")

        return None

    def create_connection(self, source_id, destination_id, **kwargs) -> None:
        """Create a new connection in the Airbyte API."""
        url = f"{self.base_url}/v1/connections"
        headers = {"Content-Type": "application/json"}
        payload = {
            "sourceId": source_id,
            "destinationId": destination_id,
        }
        payload.update(kwargs)
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Connection created successfully")
        else:
            raise Exception(f"Failed to create connection: {response.content}")

        return None

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

        return None

    def list_sources(self, limit: int = 20, offset: int = 0) -> str:
        """List sources in the Airbyte API."""
        url = f"{self.base_url}/v1/sources"
        params = {"includeDeleted": False, "limit": limit, "offset": offset}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return str(response.content)
        else:
            raise Exception(f"Failed to list sources: {response.content}")

    def create_source(self, name, workspace_id, configuration, **kwargs) -> None:
        """Create a new source in the Airbyte API."""
        url = f"{self.base_url}/v1/sources"
        payload = {
            "name": name,
            "workspaceId": workspace_id,
            "configuration": configuration,
        }
        payload.update(kwargs)
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Source created successfully")
        else:
            raise Exception(f"Failed to create source: {response.content}")

        return None
