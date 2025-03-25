"""
API Client for interacting with Airbyte, a data integration platform.
This client provides methods to update sources, create connections,
delete connections, list sources, and create sources within an Airbyte instance.
"""

import os
import time
import logging
import asyncio
from typing import Optional, Dict, Any, List, Union
from datetime import datetime

import requests
import aiohttp
from pydantic import BaseModel, Field, validator
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from prometheus_client import Counter, Histogram
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import yaml
import cachetools
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from circuitbreaker import circuit
from typing import Callable
import aiocache
from functools import wraps
import jwt
import secrets
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

# Metrics
SYNC_DURATION = Histogram('airbyte_sync_duration_seconds', 'Duration of sync jobs')
API_REQUESTS = Counter('airbyte_api_requests_total', 'Total API requests made')

load_dotenv()

class ConnectionStatus(BaseModel):
    status: str
    last_sync: Optional[datetime]
    latest_status: Dict[str, Any]

class WorkspaceDetails(BaseModel):
    workspace_id: str
    name: str
    settings: Dict[str, Any]

@dataclass
class SyncJob:
    connection_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    records_synced: int = 0

class SourceSchema(BaseModel):
    name: str
    sourceDefinitionId: str
    workspaceId: str
    connectionConfiguration: Dict[str, Any]

    @validator('connectionConfiguration')
    def validate_config(cls, v):
        required_fields = {'api_key', 'start_date'}
        if not all(field in v for field in required_fields):
            raise ValueError(f"Missing required fields: {required_fields - v.keys()}")
        return v

class PremiumFeatureException(Exception):
    """Exception for premium feature access"""

def premium_feature(func):
    """Decorator to mark premium features"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self.is_premium:
            raise PremiumFeatureException(
                f"{func.__name__} is only available in the premium version"
            )
        return await func(self, *args, **kwargs)
    return wrapper

class SecurityConfig(BaseModel):
    api_key_rotation_days: int = 30
    max_failed_attempts: int = 5
    encryption_key: str = Field(default_factory=lambda: Fernet.generate_key().decode())
    license_key: Optional[str] = None

class AirbyteApiClient:
    """Airbyte API Client with expanded functionality."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        max_retries: int = 3,
        rate_limit_per_second: int = 10,
        is_premium: bool = False,
        enterprise_config: Optional[Dict] = None,
        security_config: Optional[SecurityConfig] = None
    ) -> None:
        self.base_url = base_url or os.getenv("AIRBYTE_BASE_URL", "https://api.airbyte.com/v1")
        self.username = username or os.getenv("BASIC_AUTH_USERNAME")
        self.password = password or os.getenv("BASIC_AUTH_PASSWORD")

        if not all([self.base_url, self.username, self.password]):
            raise ValueError("Missing required configuration: base_url, username, and password are required")

        self.auth = HTTPBasicAuth(self.username, self.password)
        self.logger = logging.getLogger(__name__)
        self.rate_limit = rate_limit_per_second
        self._last_request_time = 0
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        # Add caching
        self.cache = cachetools.TTLCache(maxsize=100, ttl=300)  # 5 minutes TTL
        self.async_cache = aiocache.SimpleMemoryCache()

        # Add tracing
        self.tracer = trace.get_tracer(__name__)

        # Add connection pool
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=20),
            timeout=aiohttp.ClientTimeout(total=30)
        )

        self.is_premium = is_premium
        self.enterprise_config = enterprise_config or {}
        self.security_config = security_config or SecurityConfig()
        self._failed_attempts = 0
        self._fernet = Fernet(self.security_config.encryption_key.encode())
        self.audit_logger = logging.getLogger("airbyte.audit")

        if not self._verify_license():
            raise LicenseException("Invalid or expired license key")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def _cache_key(self, method: str, endpoint: str, **kwargs) -> str:
        """Generate cache key from request parameters."""
        return f"{method}:{endpoint}:{hash(str(kwargs))}"

    @circuit(failure_threshold=5, recovery_timeout=60)
    async def _make_async_request(self, method: str, endpoint: str, use_cache: bool = True, **kwargs) -> Dict[str, Any]:
        """Enhanced async request with caching and tracing."""
        cache_key = self._cache_key(method, endpoint, **kwargs)

        if use_cache:
            cached_response = await self.async_cache.get(cache_key)
            if cached_response:
                return cached_response

        with self.tracer.start_as_current_span(f"airbyte_{endpoint}") as span:
            try:
                response = await super()._make_async_request(method, endpoint, **kwargs)
                span.set_status(Status(StatusCode.OK))

                if use_cache:
                    await self.async_cache.set(cache_key, response, ttl=300)

                return response
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR), str(e))
                raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry mechanism and rate limiting."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, auth=self.auth, **kwargs)

        try:
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.HTTPError as e:
            raise Exception(f"API request failed: {response.content}") from e

    def update_source(
        self,
        source_id: str,
        name: str,
        workspace_id: str,
        connection_configuration: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a source in the Airbyte API."""
        return self._make_request(
            "POST",
            "sources/update",
            json={
                "sourceId": source_id,
                "name": name,
                "workspaceId": workspace_id,
                "connectionConfiguration": connection_configuration,
            }
        )

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

    async def check_connection_status(self, connection_id: str) -> ConnectionStatus:
        """Get the status of a connection including sync status."""
        result = await self._make_async_request(
            "POST",
            "connections/get",
            json={"connectionId": connection_id}
        )
        return ConnectionStatus(**result)

    async def trigger_sync(self, connection_id: str) -> Dict[str, Any]:
        """Trigger a manual sync for a connection."""
        return await self._make_async_request(
            "POST",
            "connections/sync",
            json={"connectionId": connection_id}
        )

    def get_workspace_details(self, workspace_id: str) -> WorkspaceDetails:
        """Get detailed information about a workspace."""
        result = self._make_request(
            "POST",
            "workspaces/get",
            json={"workspaceId": workspace_id}
        )
        return WorkspaceDetails(**result)

    async def list_destinations(self, workspace_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """List all destinations in a workspace."""
        return await self._make_async_request(
            "POST",
            "destinations/list",
            json={"workspaceId": workspace_id, "limit": limit}
        )

    def create_destination(
        self,
        name: str,
        workspace_id: str,
        destination_definition_id: str,
        connection_configuration: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new destination."""
        return self._make_request(
            "POST",
            "destinations/create",
            json={
                "name": name,
                "workspaceId": workspace_id,
                "destinationDefinitionId": destination_definition_id,
                "connectionConfiguration": connection_configuration
            }
        )

    async def batch_operation(self, operation: Callable, items: List[Any], batch_size: int = 50) -> List[Any]:
        """Execute operations in batches for better performance."""
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[operation(item) for item in batch],
                return_exceptions=True
            )
            results.extend(batch_results)
        return results

    async def health_check(self) -> bool:
        """Check the health of the Airbyte API."""
        try:
            await self._make_async_request("GET", "health", use_cache=False)
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return False

    async def bulk_sync(self, connection_ids: List[str], max_concurrent: int = 5) -> List[SyncJob]:
        """Optimized bulk sync with batching and monitoring."""
        return await self.batch_operation(
            self._sync_and_monitor,
            connection_ids,
            batch_size=max_concurrent
        )

    async def export_connection_configs(self, workspace_id: str, output_file: str):
        """Export all connection configurations to YAML."""
        sources = await self.list_sources(workspace_id)
        destinations = await self.list_destinations(workspace_id)

        config = {
            'workspace_id': workspace_id,
            'sources': sources,
            'destinations': destinations,
            'connections': []
        }

        with open(output_file, 'w') as f:
            yaml.dump(config, f)

    def generate_sync_report(self, sync_jobs: List[SyncJob]) -> pd.DataFrame:
        """Generate a pandas DataFrame with sync statistics."""
        return pd.DataFrame([
            {
                'connection_id': job.connection_id,
                'status': job.status,
                'duration': (job.end_time - job.start_time).total_seconds(),
                'records_synced': job.records_synced
            }
            for job in sync_jobs
        ])

    @retry(stop=stop_after_attempt(3))
    async def _wait_for_sync_completion(self, connection_id: str) -> Dict[str, Any]:
        """Wait for a sync job to complete and return its status."""
        while True:
            status = await self.check_connection_status(connection_id)
            if status.status in ['SUCCEEDED', 'FAILED']:
                return status.dict()
            await asyncio.sleep(10)

    @premium_feature
    async def advanced_monitoring(self) -> Dict[str, Any]:
        """Premium feature: Advanced monitoring with ML-based anomaly detection"""
        metrics = await self._collect_advanced_metrics()
        anomalies = self._detect_anomalies(metrics)
        return {"metrics": metrics, "anomalies": anomalies}

    @premium_feature
    async def auto_optimization(self) -> Dict[str, Any]:
        """Premium feature: Automatic optimization of sync schedules"""
        current_schedules = await self._analyze_sync_patterns()
        optimized_schedules = self._optimize_schedules(current_schedules)
        return optimized_schedules

    def _verify_license(self) -> bool:
        """Verify the license key and features"""
        if not self.security_config.license_key:
            return not self.is_premium  # Allow community version without license

        try:
            decoded = jwt.decode(
                self.security_config.license_key,
                "your-secret-key",  # In production, use proper key management
                algorithms=["HS256"]
            )
            return (
                decoded["exp"] > datetime.utcnow().timestamp() and
                decoded["is_premium"] >= self.is_premium
            )
        except jwt.InvalidTokenError:
            return False

    def _audit_log(self, action: str, details: Dict[str, Any]) -> None:
        """Log security-relevant actions"""
        self.audit_logger.info(
            f"Security event: {action}",
            extra={
                "timestamp": datetime.utcnow().isoformat(),
                "user": self.username,
                "action": action,
                "details": self._fernet.encrypt(str(details).encode()).decode(),
            }
        )

    async def rotate_api_key(self) -> str:
        """Generate new API key and invalidate old one"""
        new_key = secrets.token_urlsafe(32)
        self._audit_log("api_key_rotation", {"timestamp": datetime.utcnow().isoformat()})
        return new_key
