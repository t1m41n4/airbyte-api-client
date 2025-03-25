async function loadPipelines() {
    const response = await fetch('/api/v1/pipelines');
    const pipelines = await response.json();

    const pipelineList = document.getElementById('pipeline-list');
    pipelineList.innerHTML = pipelines.map(pipeline => `
        <div class="pipeline-card">
            <h3>${pipeline.name}</h3>
            <p>Status: ${pipeline.status}</p>
            <p>Last Sync: ${pipeline.last_sync}</p>
            <button onclick="viewMetrics('${pipeline.id}')">View Metrics</button>
        </div>
    `).join('');
}

async function createPipeline() {
    const config = {
        name: "New Pipeline",
        source_type: "postgres",
        destination_type: "snowflake",
        sync_frequency: "hourly",
        pricing_tier: "professional"
    };

    const response = await fetch('/api/v1/pipelines', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(config)
    });

    if (response.ok) {
        loadPipelines();
    }
}

async function viewMetrics(pipelineId) {
    const response = await fetch(`/api/v1/pipelines/${pipelineId}/metrics`);
    const metrics = await response.json();

    Plotly.newPlot('metrics-dashboard', [
        {
            x: metrics.timestamps,
            y: metrics.records_synced,
            type: 'line',
            name: 'Records Synced'
        }
    ]);
}

// Load pipelines on page load
document.addEventListener('DOMContentLoaded', loadPipelines);
