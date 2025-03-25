import pytest
from monitoring import AirbyteMonitoring, PerformanceMetrics

def test_performance_metrics():
    monitor = AirbyteMonitoring()
    metrics = monitor.get_performance_metrics()
    assert isinstance(metrics, PerformanceMetrics)
    assert 0 <= metrics.cpu_usage <= 100
    assert 0 <= metrics.memory_usage <= 100

def test_alert_threshold():
    monitor = AirbyteMonitoring()
    alert_called = False

    def mock_alert(message):
        nonlocal alert_called
        alert_called = True

    monitor.alert_on_threshold(90, 80, mock_alert)
    assert alert_called
