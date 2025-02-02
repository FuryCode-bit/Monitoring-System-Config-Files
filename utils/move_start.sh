#!/bin/bash

# Define the directories containing the services
service_dirs=(
    "/home/fury/Documents/ubuntu/services/SOA/"
    "/home/fury/Documents/ubuntu/services/SOA/consumers/"
    "/home/fury/Documents/ubuntu/services/SOA/service/"
)

# Loop through each directory
for dir in "${service_dirs[@]}"; do
    # Check if the directory exists
    if [ -d "$dir" ]; then
        echo "Processing directory: $dir"
        
        # Loop through each .service file in the directory
        for service_file in "$dir"*.service; do
            if [ -f "$service_file" ]; then
                # Move the service file to /etc/systemd/system/
                echo "Moving $service_file to /etc/systemd/system/"
                sudo mv "$service_file" /etc/systemd/system/
                
                # Reload systemd to recognize the new service
                echo "Reloading systemd daemon..."
                sudo systemctl daemon-reload
                
                # Start the service
                service_name=$(basename "$service_file")
                echo "Starting service: $service_name"
                sudo systemctl start "$service_name"
                
                # Enable the service to start on boot
                echo "Enabling service to start on boot..."
                sudo systemctl enable "$service_name"
                
                echo "$service_name has been moved, started, and enabled."
            else
                echo "No .service files found in $dir"
            fi
        done
    else
        echo "Directory $dir does not exist!"
    fi
done

echo "All services have been processed."
