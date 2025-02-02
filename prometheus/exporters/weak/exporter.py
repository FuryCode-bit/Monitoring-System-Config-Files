# https://grafana.com/docs/grafana-cloud/send-data/metrics/metrics-prometheus/prometheus-config-examples/wazuh-inc-wazuh-kibana/
# https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/monitoring-log-files.html

import logging
import socket
from datetime import datetime
import psutil
import requests
from prometheus_client import start_http_server, Gauge, Counter
import time

hostname = socket.gethostname()

# Custom logging filter to add machine name, timestamp, and wing
class MachineFilter(logging.Filter):
    def filter(self, record):
        # Get current time and format it
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record.formatted_datetime = current_datetime
        record.machine = hostname
        record.wing = "SOUTH"
        return record

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create two handlers: one for INFO and one for WARNING
info_handler = logging.FileHandler('/var/log/prometheus_exporter.log')
info_handler.setLevel(logging.INFO)

warning_handler = logging.FileHandler('/var/log/prometheus_exporter.log')
warning_handler.setLevel(logging.WARNING)

# Create a common formatter for both INFO and WARNING logs
formatter = logging.Formatter('[%(formatted_datetime)s]: Wing: %(wing)s, Machine: %(machine)s - %(message)s')
info_handler.setFormatter(formatter)
warning_handler.setFormatter(formatter)

# Add the custom filter to both handlers
info_handler.addFilter(MachineFilter())
warning_handler.addFilter(MachineFilter())

# Add both handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(warning_handler)

import psutil
import requests
from prometheus_client import start_http_server, Gauge, Counter
import time

cpu_usage_gauge = Gauge('system_cpu_usage_percent', 'Percentage of CPU usage')
memory_usage_gauge = Gauge('system_memory_usage_percent', 'Percentage of memory usage')
http_requests_received_counter = Counter('http_requests_received_total', 'Total number of HTTP requests received', ['method'])
http_requests_sent_counter = Counter('http_requests_sent_total', 'Total number of HTTP requests sent', ['method'])
request_latency_total_gauge = Gauge('http_request_latency_total_seconds', 'Total time for processing a batch of 10 HTTP requests')
request_latency_avg_gauge = Gauge('http_request_latency_avg_seconds', 'Average time for processing a batch of 10 HTTP requests')

def collect_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_usage_gauge.set(cpu_usage)
    logging.info(f"CPU usage: {cpu_usage}%")
    
    if cpu_usage > 90:
        logging.warning(f"High CPU usage detected: {cpu_usage}%")

    memory_usage = psutil.virtual_memory().percent
    memory_usage_gauge.set(memory_usage)
    logging.info(f"Memory usage: {memory_usage}%")
    
    if memory_usage > 90:
        logging.warning(f"High memory usage detected: {memory_usage}%")

def track_http_requests():
    url = "http://0.0.0.0:80/"
    
    start_time = time.time()

    for _ in range(10):
        response = requests.get(url)
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    request_latency_total_gauge.set(elapsed_time)
    avg_latency = elapsed_time / 10
    request_latency_avg_gauge.set(avg_latency)

    if avg_latency > 0.3:
        logging.warning(f"High average request processing time: {avg_latency} seconds per request for 10 requests")

def main():
    start_http_server(8000)
    
    logging.info("Prometheus Exporter started.")
    
    while True:
        collect_system_metrics()
        track_http_requests()
        time.sleep(5)

if __name__ == '__main__':
    main()