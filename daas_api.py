from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from typing import List
from daas_service import DataService, DataServiceConfig

app = FastAPI(title="Data as a Service API")
api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/api/v1/pipelines")
async def create_pipeline(
    config: DataServiceConfig,
    api_key: str = Depends(api_key_header)
):
    """Create a new data pipeline"""
    service = DataService()
    return await service.create_data_pipeline(config)

@app.get("/api/v1/pipelines/{pipeline_id}/metrics")
async def get_pipeline_metrics(
    pipeline_id: str,
    api_key: str = Depends(api_key_header)
):
    """Get pipeline metrics"""
    service = DataService()
    return await service.get_pipeline_metrics(pipeline_id)
