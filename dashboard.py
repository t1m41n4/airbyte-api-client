from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
import plotly.express as px
import pandas as pd

app = FastAPI(title="Airbyte Manager Dashboard")
api_key_header = APIKeyHeader(name="X-API-Key")

class Dashboard:
    def __init__(self, client):
        self.client = client
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        @app.get("/api/metrics")
        async def get_metrics(api_key: str = Depends(api_key_header)):
            metrics = await self.client.get_performance_metrics()
            return metrics

        @app.get("/api/sync-status")
        async def get_sync_status(api_key: str = Depends(api_key_header)):
            jobs = await self.client.bulk_sync(self.client.get_all_connections())
            return self.client.generate_sync_report(jobs).to_dict()

    def start(self, port: int = 8000):
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port)
