from typing import Dict, List, Any
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from airbyte_manage import AirbyteApiClient

class DataServiceConfig(BaseModel):
    name: str
    source_type: str
    destination_type: str
    sync_frequency: str
    transformation_rules: Dict[str, Any] = {}
    pricing_tier: str = "basic"

class DataService:
    def __init__(self, client: AirbyteApiClient):
        self.client = client
        self.pricing = {
            "basic": {"price": 99, "sync_frequency": "daily", "support": "email"},
            "professional": {"price": 299, "sync_frequency": "hourly", "support": "priority"},
            "enterprise": {"price": 999, "sync_frequency": "real-time", "support": "dedicated"}
        }

    async def create_data_pipeline(self, config: DataServiceConfig) -> Dict[str, Any]:
        """Create a complete data pipeline for a customer"""
        source = await self.client.create_source(
            name=f"{config.name}_source",
            sourceDefinitionId=config.source_type,
            connectionConfiguration=config.transformation_rules
        )

        destination = await self.client.create_destination(
            name=f"{config.name}_destination",
            destination_definition_id=config.destination_type
        )

        connection = await self.client.create_connection(
            connection_name=config.name,
            source_id=source["sourceId"],
            destination_id=destination["destinationId"],
            sync_frequency=self.pricing[config.pricing_tier]["sync_frequency"]
        )

        return {
            "pipeline_id": connection["connectionId"],
            "status": "active",
            "pricing_tier": config.pricing_tier,
            "monthly_cost": self.pricing[config.pricing_tier]["price"]
        }

    async def get_pipeline_metrics(self, pipeline_id: str) -> Dict[str, Any]:
        """Get analytics for a data pipeline"""
        status = await self.client.check_connection_status(pipeline_id)
        metrics = await self.client.advanced_monitoring()

        return {
            "status": status.status,
            "records_synced": metrics.get("records_synced", 0),
            "last_sync": status.last_sync,
            "performance_metrics": metrics
        }
