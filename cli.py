import click
import asyncio
import yaml
from rich.console import Console
from rich.table import Table
from airbyte_manage import AirbyteApiClient

console = Console()

@click.group()
def cli():
    """Airbyte API CLI tool"""
    pass

@cli.command()
@click.argument('connections_file')
@click.option('--max-concurrent', default=5, help='Maximum concurrent syncs')
def bulk_sync(connections_file: str, max_concurrent: int):
    """Execute bulk sync from a YAML configuration file."""
    with open(connections_file) as f:
        config = yaml.safe_load(f)

    client = AirbyteApiClient()
    jobs = asyncio.run(client.bulk_sync(config['connections'], max_concurrent))

    table = Table(title="Sync Results")
    table.add_column("Connection ID")
    table.add_column("Status")
    table.add_column("Duration (s)")
    table.add_column("Records Synced")

    for job in jobs:
        table.add_row(
            job.connection_id,
            job.status,
            str((job.end_time - job.start_time).total_seconds()),
            str(job.records_synced)
        )

    console.print(table)

if __name__ == '__main__':
    cli()
