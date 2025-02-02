#!/bin/bash

# List of services to stop
services=(
    "bridge.service"
    "celsius.service"
    "consumercelsius.service"
    "consumerfarenheit.service"
    "farenheit.service"
    "prom.service"
    "registry.service"
    "sensor.service"
)

# Loop through each service and stop it
for service in "${services[@]}"; do
    echo "Stopping $service..."
    sudo systemctl stop "$service"
    
    # Check if the service was stopped successfully
    if systemctl is-active --quiet "$service"; then
        echo "$service failed to stop."
    else
        echo "$service stopped successfully."
    fi
done

echo "All services have been processed."