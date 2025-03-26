from dataclasses import dataclass
from datetime import datetime
import psutil
from typing import Callable
from prometheus_client import Gauge, Histogram, Counter


@dataclass
class PerformanceMetrics:
    cpu_usage: float
    memory_usage: float
    active_connections: int
    cache_hit_rate: float
    average_response_time: float


class AirbyteMonitoring:
    def __init__(self):
        self.performance_gauge = Gauge(
            'airbyte_client_performance',
            'Performance metrics for Airbyte client',
            ['metric_name']
        )

        self.response_times = Histogram(
            'airbyte_response_time',
            'Response times for Airbyte API calls',
            ['endpoint']
        )

        self.error_counter = Counter(
            'airbyte_errors_total',
            'Total number of errors',
            ['error_type']
        )
        self._start_time = datetime.now()

    def get_performance_metrics(self) -> PerformanceMetrics:
        return PerformanceMetrics(
            cpu_usage=psutil.cpu_percent(),
            memory_usage=psutil.virtual_memory().percent,
            active_connections=len(psutil.net_connections()),
            cache_hit_rate=self._calculate_cache_hit_rate(),
            average_response_time=self.response_times.observe()
        )

    def _calculate_cache_hit_rate(self) -> float:
        # Implementation for cache hit rate calculation
        pass

    def alert_on_threshold(self, metric: float, threshold: float, alert_func: Callable):
        if metric > threshold:
            alert_func(f"Metric {metric} exceeded threshold {threshold}")
