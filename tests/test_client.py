import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from airbyte_manage import AirbyteApiClient, ConnectionStatus, SecurityConfig

@pytest.fixture
def client():
    return AirbyteApiClient(
        base_url="http://test",
        username="test",
        password="test",
        is_premium=True,
        security_config=SecurityConfig(license_key="test-key")
    )

@pytest.mark.asyncio
async def test_create_source(client):
    with patch.object(client, '_make_request') as mock_request:
        mock_request.return_value = {"sourceId": "test-source"}
        result = await client.create_source(
            name="test",
            workspaceId="test-workspace",
            sourceDefinitionId="test-definition",
            connectionConfiguration={"api_key": "test", "start_date": "2024-01-01"}
        )
        assert result["sourceId"] == "test-source"

@pytest.mark.asyncio
async def test_bulk_sync(client):
    with patch.object(client, '_make_async_request') as mock_request:
        mock_request.return_value = {"status": "succeeded"}
        result = await client.bulk_sync(["conn1", "conn2"])
        assert len(result) == 2
        assert all(job.status == "succeeded" for job in result)

@pytest.mark.asyncio
async def test_advanced_monitoring(client):
    with patch.object(client, '_make_async_request') as mock_request:
        mock_request.return_value = {"metrics": {}, "anomalies": []}
        result = await client.advanced_monitoring()
        assert "metrics" in result
        assert "anomalies" in result

@pytest.mark.asyncio
async def test_connection_status(client):
    mock_status = {
        "status": "running",
        "last_sync": "2024-01-01T00:00:00Z",
        "latest_status": {}
    }
    with patch.object(client, '_make_async_request', return_value=mock_status):
        result = await client.check_connection_status("test-conn")
        assert isinstance(result, ConnectionStatus)
        assert result.status == "running"

def test_security_config(client):
    with pytest.raises(Exception):
        AirbyteApiClient(is_premium=True)  # Should fail without license

@pytest.mark.asyncio
async def test_api_key_rotation(client):
    new_key = await client.rotate_api_key()
    assert len(new_key) > 32  # Minimum key length

def test_cache_operations(client):
    test_data = {"test": "data"}
    key = client._cache_key("GET", "test", param="value")
    client.cache.set(key, test_data)
    assert client.cache.get(key) == test_data
