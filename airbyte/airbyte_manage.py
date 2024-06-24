"""
API Client for interacting with Airbyte, a data integration platform.
This client provides methods to update sources, create connections,
delete connections, list sources, and create sources within an Airbyte instance.
"""

import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()


class AirbyteApiClient:
    """Airbyte API Client."""

    def __init__(
        self,
        base_url=None,
    ) -> None:
        self.base_url = base_url or os.getenv("AIRBYTE_BASE_URL")
        self.workspaceId = os.getenv("AIRBYTE_WORKSPACE_ID")
        self.name = os.getenv("SOURCE_NAME")
        self.access_key = os.getenv("ACCESS_KEY")
        self.start_date = os.getenv("START_DATE")
        self.page_size = int(os.getenv("PAGE_SIZE", "0"))
        self.destination_name = os.getenv("AIRBYTE_DESTINATION_NAME")
        self.destination_path = os.getenv("AIRBYTE_DESTINATION_PATH")
        self.destinationDefinitionId = os.getenv("DESTINATION_DEFINITION_ID")
        self.sourceDefinitionId = os.getenv("DEFINITION_ID")
        self.sourceType = os.getenv("SOURCE_TYPE")
        self.username = os.getenv("BASIC_AUTH_USERNAME")
        self.password = os.getenv("BASIC_AUTH_PASSWORD")
        self.base = os.getenv("BASE")
        self.api_key = os.getenv("API_KEY")
        self.destinationDefinitionId = os.getenv("DESTINATION_DEFINITION_ID")
        self.destination_path = os.getenv("DESTINATION_PATH")
        self.destination_name = os.getenv("AIRBYTE_DESTINATION_NAME")
        self.connection_name = os.getenv("CONNECTION_NAME")
        self.namespaceDefinition = os.getenv("NAMESPACE_DEFINITION")
        self.sourceId = os.getenv("SOURCE_ID")
        self.connection_id = os.getenv("CONNECTION_ID")
        self.destinationId = os.getenv("DESTINATION_ID")

    def get_source_configuration(self) -> dict:
        """Get the configuration for the source."""
        return {
            "sourceType": self.sourceType,
            "start_date": self.start_date,
            "access_key": self.access_key,
            "base": self.base,
            "page_size": self.page_size,
            "api_key": self.api_key,
        }

    def update_source_configuration(self) -> dict:
        """Get the configuration for the source."""
        return {
            "start_date": self.start_date,
            "access_key": self.access_key,
            "page_size": self.page_size,
            "api_key": self.api_key,
        }

    def update_source(
        self, source_id, name, workspace_id, connectionConfiguration: dict
    ) -> None:
        """Update a source in the Airbyte API."""
        connectionConfiguration = self.get_source_configuration()
        url = f"{self.base_url}/sources/update"
        payload = {
            "sourceId": source_id,
            "name": name,
            "workspaceId": workspace_id,
            "connectionConfiguration": connectionConfiguration,
        }
        auth = HTTPBasicAuth(self.username, self.password)
        response = requests.post(url, json=payload, auth=auth)
        if response.status_code == 200:
            print(f"Source {source_id} updated successfully")
        else:
            raise Exception(f"Failed to update source {source_id}: {response.content}")

        return None

    def create_connection(
        self,
        workspaceId,
        connection_name,
        source_id,
        destination_id,
        namespaceDefinition,
        **kwargs,
    ) -> None:
        """Create a new connection in the Airbyte API."""
        url = f"{self.base_url}/connections/create"
        payload = {
            "workspaceId": workspaceId,
            "name": connection_name,
            "sourceId": source_id,
            "destinationId": destination_id,
            "namespaceDefinition": namespaceDefinition,
        }
        payload.update(kwargs)
        auth = HTTPBasicAuth(self.username, self.password)
        response = requests.post(url, json=payload, auth=auth)
        if response.status_code == 200:
            print("Connection created successfully")
        else:
            raise Exception(f"Failed to create connection: {response.content}")

        return None

    def delete_connection(self, connection_id) -> None:
        """Delete a connection in the Airbyte API."""
        url = f"{self.base_url}/connections/delete"
        payload = {
            "connectionId": connection_id,
        }
        auth = HTTPBasicAuth(self.username, self.password)
        response = requests.post(url, json=payload, auth=auth)
        if response.status_code == 204:
            print(f"Connection {connection_id} deleted successfully")
        else:
            raise Exception(
                f"Failed to delete connection {connection_id}: {response.content}"
            )

        return None

    def list_sources(self, limit: int = 20, offset: int = 0) -> str:
        """List sources in the Airbyte API."""
        url = f"{self.base_url}/sources/list"
        payload = {"workspaceId": self.workspaceId}
        params = {"includeDeleted": False, "limit": limit, "offset": offset}
        auth = HTTPBasicAuth(self.username, self.password)
        response = requests.post(url, params=params, json=payload, auth=auth)
        if response.status_code == 200:
            return str(response.content)
        else:
            raise Exception(f"Failed to list sources: {response.content}")

    def create_source(
        self,
        name,
        workspaceId,
        sourceDefinitionId,
        connectionConfiguration: dict,
        **kwargs,
    ) -> None:
        """Create a new source in the Airbyte API."""
        connectionConfiguration = self.get_source_configuration()
        url = f"{self.base_url}/sources/create"
        payload = {
            "workspaceId": workspaceId,
            "name": name,
            "sourceDefinitionId": sourceDefinitionId,
            "connectionConfiguration": connectionConfiguration,
        }
        payload.update(kwargs)
        auth = HTTPBasicAuth(self.username, self.password)
        response = requests.post(url, json=payload, auth=auth)

        if response.status_code == 200:
            print("Source created successfully")
        else:
            raise Exception(f"Failed to create source: {response.content}")

        return None
