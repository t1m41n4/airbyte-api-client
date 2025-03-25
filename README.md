# Airbyte API Client

A Python client for interacting with the Airbyte API. This client provides methods to update sources,
create connections, delete connections, list sources, and create sources, facilitating easy
integration and management of data sync processes within Airbyte.

## Features

- Asynchronous API support
- Automatic retry mechanism
- Rate limiting protection
- Connection status monitoring
- Workspace management
- Destination management
- Comprehensive logging
- Type-safe responses using Pydantic

## Installation

```bash
pip install airbyte-api-client
```

## Configuration

The client can be configured using environment variables or direct initialization:

```python
from airbyte_api_client import AirbyteApiClient

# Using environment variables
api_client = AirbyteApiClient()

# Direct initialization
api_client = AirbyteApiClient(
    base_url="https://your-airbyte-instance/api/v1",
    username="your-username",
    password="your-password"
)
```

### Environment Variables

- `AIRBYTE_BASE_URL`: Base URL of your Airbyte instance
- `BASIC_AUTH_USERNAME`: Username for Basic Authentication
- `BASIC_AUTH_PASSWORD`: Password for Basic Authentication

## Usage Examples

```python
# Create a source
source = api_client.create_source(
    name="My Source",
    workspace_id="workspace-uuid",
    source_definition_id="source-definition-uuid",
    connection_configuration={
        "api_key": "your-api-key",
        "start_date": "2023-01-01"
    }
)

# Create a connection
connection = api_client.create_connection(
    workspace_id="workspace-uuid",
    connection_name="My Connection",
    source_id="source-uuid",
    destination_id="destination-uuid",
    namespace_definition="source"
)

# List sources
sources = api_client.list_sources(limit=20, offset=0)
```

## Advanced Usage

### Async Operations

```python
import asyncio

async def main():
    client = AirbyteApiClient()

    # Check connection status
    status = await client.check_connection_status("connection-id")
    print(f"Connection status: {status.status}")

    # Trigger manual sync
    await client.trigger_sync("connection-id")

    # List destinations
    destinations = await client.list_destinations("workspace-id")
    print(f"Found {len(destinations)} destinations")

asyncio.run(main())
```

### Workspace Management

```python
# Get workspace details
workspace = client.get_workspace_details("workspace-id")
print(f"Workspace name: {workspace.name}")

# Create destination
destination = client.create_destination(
    name="My Destination",
    workspace_id="workspace-id",
    destination_definition_id="destination-definition-id",
    connection_configuration={
        "host": "localhost",
        "port": 5432,
        "database": "mydb"
    }
)
```

## Advanced Features

### Parallel Sync Operations
```python
# Bulk sync multiple connections
connections = ["conn-1", "conn-2", "conn-3"]
results = await client.bulk_sync(connections, max_concurrent=5)
```

### Automated Scheduling
```python
# Schedule recurring syncs
client.schedule_sync("connection-id", "0 */6 * * *")  # Run every 6 hours
```

### Configuration Management
```python
# Export workspace configuration
await client.export_connection_configs("workspace-id", "config.yaml")
```

### Metrics and Reporting
```python
# Generate sync report
jobs = await client.bulk_sync(connections)
report = client.generate_sync_report(jobs)
print(report.describe())
```

### CLI Usage
```bash
# Run bulk sync from config file
python -m airbyte_api_client bulk-sync config.yaml --max-concurrent 5
```

## Performance Features

- Parallel processing for bulk operations
- Automatic retry mechanism with exponential backoff
- Rate limiting protection
- Prometheus metrics integration
- Background job scheduling
- Async/await support for improved performance

## Best Practices

- Use bulk operations for multiple syncs
- Monitor metrics for performance optimization
- Schedule syncs during off-peak hours
- Export configurations for backup and version control
- Use the CLI for automated tasks

## API Documentation

For more details on the Airbyte API, refer to the [official documentation](https://reference.airbyte.com/reference/).

## Changes

- Updated base URL and HTTP methods for endpoints to align with new API standards.
- Enhanced `update_source` method to support additional parameters using **kwargs.
- Improved `create_connection` method to handle JSON payload more efficiently.
- Simplified `delete_connection` method by removing explicit return type.
- Optimized `list_sources` method to use `requests.get` directly for improved performance.
- Refactored `create_source` method to use `requests.post` for clearer code structure and consistency.
- Improved error handling and response messaging throughout the API client.
- Added support for environment variables to configure API client parameters.
- Implemented HTTP Basic Authentication for secure API requests.
- Set default `base_url` to 'https://api.airbyte.com/v1'

## Premium Features

The premium version includes:

### Advanced Monitoring
- ML-based anomaly detection
- Predictive failure analysis
- Custom alerting integrations
- Real-time monitoring dashboard

### Automation
- Intelligent sync scheduling
- Auto-optimization of configurations
- Batch operations at scale
- Priority support

### Enterprise Support
- Custom SLAs
- Dedicated support
- Custom feature development
- On-premises deployment support

## Pricing Plans

1. **Community Edition (Free)**
   - Basic sync operations
   - Standard monitoring
   - Community support

2. **Professional ($299/month)**
   - All Community features
   - Advanced monitoring
   - Dashboard access
   - Email support

3. **Enterprise (Custom pricing)**
   - All Professional features
   - Custom features
   - Premium support
   - On-premises deployment

## Getting Started with Premium Features

```python
client = AirbyteApiClient(
    is_premium=True,
    enterprise_config={
        "sla_level": "premium",
        "support_email": "enterprise@example.com"
    }
)

# Use advanced monitoring
anomalies = await client.advanced_monitoring()

# Auto-optimize sync schedules
optimized = await client.auto_optimization()
```

## Use Cases

### 1. Data Migration Projects
```python
async with AirbyteApiClient() as client:
    # Setup source database
    source = await client.create_source(
        name="Production PostgreSQL",
        workspace_id="workspace-123",
        source_definition_id="postgresql",
        connection_configuration={
            "host": "prod-db.example.com",
            "port": 5432,
            "database": "production",
            "username": "readonly_user",
            "password": "secret"
        }
    )

    # Setup destination data warehouse
    destination = await client.create_destination(
        name="Snowflake Warehouse",
        workspace_id="workspace-123",
        destination_definition_id="snowflake",
        connection_configuration={
            "host": "snowflake.example.com",
            "warehouse": "COMPUTE_WH",
            "database": "ANALYTICS"
        }
    )

    # Create and monitor migration sync
    connection = await client.create_connection(
        workspace_id="workspace-123",
        connection_name="Prod DB Migration",
        source_id=source['sourceId'],
        destination_id=destination['destinationId'],
        namespaceDefinition="source"
    )
```

### 2. Automated ETL Orchestration
```python
# Schedule multiple syncs with monitoring
async def setup_daily_etl():
    client = AirbyteApiClient()

    # Schedule nightly syncs
    for conn_id in ["sales_data", "customer_data", "inventory"]:
        client.schedule_sync(conn_id, "0 0 * * *")  # Run at midnight

    # Monitor sync status
    while True:
        statuses = await client.bulk_sync(["sales_data", "customer_data", "inventory"])
        report = client.generate_sync_report(statuses)

        if any(status.status == "FAILED" for status in statuses):
            alert_team(report)

        await asyncio.sleep(3600)  # Check every hour
```

### 3. Performance Monitoring
```python
from airbyte_api_client import AirbyteApiClient
from monitoring import AirbyteMonitoring

async def monitor_sync_performance():
    client = AirbyteApiClient()
    monitor = AirbyteMonitoring()

    # Start sync
    sync_job = await client.trigger_sync("connection-123")

    # Monitor performance
    metrics = monitor.get_performance_metrics()
    print(f"CPU Usage: {metrics.cpu_usage}%")
    print(f"Memory Usage: {metrics.memory_usage}%")
    print(f"Active Connections: {metrics.active_connections}")

    # Alert on high resource usage
    monitor.alert_on_threshold(
        metric=metrics.cpu_usage,
        threshold=80.0,
        alert_func=send_slack_alert
    )
```

### 4. Bulk Operations
```python
# Export/Import workspace configurations
async def migrate_workspace(source_workspace: str, target_workspace: str):
    client = AirbyteApiClient()

    # Export current config
    await client.export_connection_configs(
        source_workspace,
        "workspace_backup.yaml"
    )

    # Create multiple connections in parallel
    connections = [
        {"source": "postgres_1", "destination": "snowflake"},
        {"source": "mysql_2", "destination": "bigquery"},
        {"source": "s3_data", "destination": "redshift"}
    ]

    results = await client.batch_operation(
        client.create_connection,
        connections,
        batch_size=3
    )
```

### 5. Health Monitoring and Maintenance
```python
async def maintain_workspace():
    client = AirbyteApiClient()

    # Check API health
    is_healthy = await client.health_check()

    if is_healthy:
        # Get workspace details
        workspace = client.get_workspace_details("workspace-123")

        # List and verify sources
        sources = await client.list_sources(workspace.workspace_id)

        # Clean up unused connections
        for source in sources:
            if source['status'] == 'deprecated':
                await client.delete_connection(source['connectionId'])
```

## Best Practices and Tips

### Rate Limiting and Performance
- Use `batch_operation` for bulk operations
- Implement proper error handling and retries
- Monitor API rate limits using the monitoring module
- Cache frequently accessed data

### Monitoring and Maintenance
- Regular health checks using `health_check()`
- Monitor sync performance with `PerformanceMetrics`
- Set up alerts for failed syncs
- Export configurations regularly for backup

### Security
- Use environment variables for sensitive credentials
- Implement proper access controls
- Regular audit of connection configurations
- Monitor for unusual activity patterns

## Security Features

### License Protection
The project uses a Business Source License (BSL) which:
- Allows free use for non-commercial purposes
- Requires a paid license for commercial use
- Converts to Apache 2.0 after 3 years
- Prevents unauthorized commercialization

### Enterprise Security Features
```python
# Initialize with security configuration
client = AirbyteApiClient(
    security_config=SecurityConfig(
        api_key_rotation_days=30,
        max_failed_attempts=5,
        license_key="your-enterprise-license"
    )
)

# Automatic API key rotation
new_key = await client.rotate_api_key()

# Encrypted audit logging
client._audit_log("sensitive_operation", {"user": "admin"})
```

### Security Best Practices
1. API Key Management
   - Automatic key rotation every 30 days
   - Secure key storage using encryption
   - Failed attempt monitoring

2. Audit Logging
   - Encrypted audit trails
   - Detailed operation logging
   - Security event monitoring

3. Access Control
   - Role-based permissions
   - IP whitelisting
   - Rate limiting

4. Data Protection
   - End-to-end encryption
   - Secure credential storage
   - Data masking

## Data as a Service Offering

Turn your data integration capabilities into a service business:

### Service Tiers

1. **Basic Tier ($99/month)**
   - Daily data syncs
   - Basic transformations
   - Email support
   - Up to 5 data sources

2. **Professional Tier ($299/month)**
   - Hourly data syncs
   - Advanced transformations
   - Priority support
   - Up to 20 data sources
   - Custom destinations

3. **Enterprise Tier ($999/month)**
   - Real-time data syncs
   - Custom transformations
   - Dedicated support
   - Unlimited sources
   - SLA guarantees

### Example: Creating a Data Pipeline

```python
from daas_service import DataService, DataServiceConfig

# Configure a new data pipeline
config = DataServiceConfig(
    name="customer_analytics",
    source_type="postgres",
    destination_type="snowflake",
    sync_frequency="hourly",
    pricing_tier="professional",
    transformation_rules={
        "include_tables": ["customers", "orders"],
        "transformations": ["clean_addresses", "calculate_ltv"]
    }
)

# Create the pipeline
service = DataService()
pipeline = await service.create_data_pipeline(config)
```

### Running the DaaS API

```bash
uvicorn daas_api:app --host 0.0.0.0 --port 8000
```

