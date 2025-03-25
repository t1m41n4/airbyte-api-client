# Getting Started

## Installation

```bash
pip install airbyte-api-client
```

## Configuration

### Environment Setup
```bash
export AIRBYTE_BASE_URL="your-airbyte-instance"
export BASIC_AUTH_USERNAME="your-username"
export BASIC_AUTH_PASSWORD="your-password"
```

### Basic Usage
```python
from airbyte_api_client import AirbyteApiClient

async def main():
    client = AirbyteApiClient()

    # Create source
    source = await client.create_source(
        name="My Database",
        workspace_id="workspace-123",
        source_definition_id="postgres",
        connection_configuration={
            "host": "localhost",
            "port": 5432,
            "database": "mydb"
        }
    )

    # Create connection
    connection = await client.create_connection(
        workspace_id="workspace-123",
        connection_name="Daily Sync",
        source_id=source["sourceId"],
        destination_id="dest-123"
    )
```

## Next Steps
1. [Read the implementation details](implementation.md)
2. [Explore premium features](premium-features.md)
3. [Review security guidelines](security.md)
4. [Check API reference](api-reference.md)
