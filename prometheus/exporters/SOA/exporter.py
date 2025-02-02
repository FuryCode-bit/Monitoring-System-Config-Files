from prometheus_client import Gauge, make_wsgi_app
from wsgiref.simple_server import make_server
import requests
import time
import threading
import pika
from requests.auth import HTTPBasicAuth

# Definition of Prometheus metrics
service_health = Gauge('service_health', 'Health status of a service', ['service_name'])
registered_services = Gauge('registry_registered_services', 'Number of services registered in the registry')
current_temperature = Gauge('temperature', 'Current temperature reported by a service', ['service_name', 'unit'])
rabbitmq_connection = Gauge('rabbitmq_connection', 'Status of RabbitMQ connection (1 = Connected, 0 = Disconnected)')
rabbitmq_queue_length = Gauge('rabbitmq_queue_length', 'Number of messages in RabbitMQ queues', ['queue_name'])

# Definition of RabbitMQ node metrics
rabbitmq_fd_used = Gauge('rabbitmq_fd_used', 'Used file descriptors', ['node'])
rabbitmq_fd_limit = Gauge('rabbitmq_fd_limit', 'File descriptors available', ['node'])
rabbitmq_mem_used = Gauge('rabbitmq_mem_used', 'Memory used in bytes', ['node'])
rabbitmq_mem_alarm = Gauge('rabbitmq_mem_alarm', 'Memory alarm status (1 = triggered, 0 = normal)', ['node'])

# Configuration
SERVICES = {
    'registry': 'http://0.0.0.0:5001',
    'celsius_service': 'http://0.0.0.0:5002',
    'fahrenheit_service': 'http://0.0.0.0:5003'
}
RABBITMQ_HOST = 'http://0.0.0.0:15672'
RABBITMQ_API = '/api'
RABBITMQ_AUTH = ('guest', 'guest')
RABBITMQ_QUEUE = 'temperature_queue'

# Function to check the health of a service
def check_service_health(service_name, service_url):
    try:
        response = requests.get(service_url, timeout=2)
        service_health.labels(service_name=service_name).set(1 if response.status_code == 200 else 0)
    except requests.exceptions.RequestException:
        service_health.labels(service_name=service_name).set(0)

# Function to get the number of registered services in the registry
def update_registered_services():
    try:
        response = requests.get(f'{SERVICES["registry"]}/services', timeout=2)
        if response.status_code == 200:
            print("response: ", response.json())
            # Parse the JSON response
            services = response.json()
            # Set the number of registered services based on the keys in the dictionary
            registered_services.set(len(services.keys()))
            print(f"Setting registered_services to {len(services.keys())}")
        else:
            # Log the unexpected response
            print(f"Unexpected response code: {response.status_code}, Body: {response.text}")
            registered_services.set(0)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching registered services: {e}")
        registered_services.set(0)

# Function to get the current temperature from a temperature service
def update_temperature(service_name, service_url):
    try:
        response = requests.get(service_url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            current_temperature.labels(service_name=service_name, unit=data.get('unit', 'Unknown')).set(data.get('temperature', 0))
        else:
            current_temperature.labels(service_name=service_name, unit='Unknown').set(0)
    except requests.exceptions.RequestException:
        current_temperature.labels(service_name=service_name, unit='Unknown').set(0)

# Function to monitor RabbitMQ connection and queue length
def update_rabbitmq_metrics():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        rabbitmq_connection.set(1)
        channel = connection.channel()

        # Fetch queue information
        queue_info = channel.queue_declare(queue=RABBITMQ_QUEUE, passive=True)
        rabbitmq_queue_length.labels(queue_name=RABBITMQ_QUEUE).set(queue_info.method.message_count)

        connection.close()
    except pika.exceptions.AMQPError:
        rabbitmq_connection.set(0)
        rabbitmq_queue_length.labels(queue_name=RABBITMQ_QUEUE).set(0)

# Function to fetch RabbitMQ node metrics via HTTP API
def update_rabbitmq_node_metrics():
    try:
        url = f'{RABBITMQ_HOST}{RABBITMQ_API}/nodes'
        response = requests.get(url, auth=HTTPBasicAuth(*RABBITMQ_AUTH), timeout=5)
        response.raise_for_status()
        nodes = response.json()

        for node in nodes:
            name = node['name']
            rabbitmq_fd_used.labels(node=name).set(node.get('fd_used', 0))
            rabbitmq_fd_limit.labels(node=name).set(node.get('fd_total', 0))
            rabbitmq_mem_used.labels(node=name).set(node.get('mem_used', 0))
            rabbitmq_mem_alarm.labels(node=name).set(1 if node.get('mem_alarm', False) else 0)
    except Exception as e:
        print(f"Error fetching RabbitMQ node metrics: {e}")

# Function to run the Prometheus metrics server
def start_metrics_server():
    app = make_wsgi_app()  # Create a WSGI app for Prometheus metrics
    with make_server('', 8100, app) as httpd:
        print("Serving metrics on http://localhost:8100/metrics")
        httpd.serve_forever()

# Function to periodically update metrics
def update_metrics():
    while True:
        # Update metrics for each service
        for service_name, service_url in SERVICES.items():
            check_service_health(service_name, service_url)

        # Update specific metrics
        update_registered_services()
        update_temperature('celsius_service', SERVICES['celsius_service'])
        update_temperature('fahrenheit_service', SERVICES['fahrenheit_service'])
        update_rabbitmq_metrics()
        update_rabbitmq_node_metrics()

        # Sleep before the next update
        time.sleep(5)

if __name__ == '__main__':
    # Start the metrics server in a separate thread
    threading.Thread(target=start_metrics_server, daemon=True).start()

    # Main loop to periodically update metrics
    update_metrics()
