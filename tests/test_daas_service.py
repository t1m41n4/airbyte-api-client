import pytest
from unittest.mock import Mock, AsyncMock, patch
from daas_service import DataService, DataServiceConfig

@pytest.fixture
def service():
    mock_client = Mock()
    mock_client.create_source = AsyncMock(return_value={"sourceId": "test"})
    mock_client.create_destination = AsyncMock(return_value={"destinationId": "test"})
    mock_client.create_connection = AsyncMock(return_value={"connectionId": "test"})
    return DataService(mock_client)

@pytest.mark.asyncio
async def test_create_pipeline(service):
    config = DataServiceConfig(
        name="test",
        source_type="postgres",
        destination_type="snowflake",
        sync_frequency="daily",
        pricing_tier="basic"
    )
    result = await service.create_data_pipeline(config)
    assert result["status"] == "active"
    assert result["pricing_tier"] == "basic"
    assert "pipeline_id" in result

@pytest.mark.asyncio
async def test_pipeline_metrics(service):
    service.client.check_connection_status = AsyncMock(
        return_value={"status": "running", "last_sync": "2024-01-01T00:00:00Z"}
    )
    service.client.advanced_monitoring = AsyncMock(
        return_value={"records_synced": 1000}
    )

    metrics = await service.get_pipeline_metrics("test-pipeline")
    assert "status" in metrics
    assert "records_synced" in metrics
