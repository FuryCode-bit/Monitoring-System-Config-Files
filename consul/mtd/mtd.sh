#!/bin/bash

# Configuration
LXC_IDS=(143 144)
ROTATION_INTERVAL=300
LOG_FILE="/var/log/proxmox_mtd.log"

# Redirect all output to the log file
exec > >(tee -a "$LOG_FILE") 2>&1

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Function to start a container
start_lxc() {
    local lxc_id=$1
    log_message "Starting LXC container $lxc_id."
    pct start "$lxc_id"
}

# Function to stop a container
stop_lxc() {
    local lxc_id=$1
    log_message "Stopping LXC container $lxc_id."
    pct stop "$lxc_id"
}

# Function to get the currently running container
get_running_lxc() {
    for lxc_id in "${LXC_IDS[@]}"; do
        local status=$(pct status "$lxc_id" | grep -o 'running')
        if [ "$status" == "running" ]; then
            echo "$lxc_id"
            return
        fi
    done
    echo ""
}

while true; do
    log_message "Starting rotation cycle."

    # Get the currently running container
    current_lxc=$(get_running_lxc)

    # Determine the next container to start
    next_lxc=""
    if [ -n "$current_lxc" ]; then
        for i in "${!LXC_IDS[@]}"; do
            if [ "${LXC_IDS[$i]}" == "$current_lxc" ]; then
                next_lxc_index=$(( (i + 1) % ${#LXC_IDS[@]} ))
                next_lxc="${LXC_IDS[$next_lxc_index]}"
                break
            fi
        done
        # Stop the current container
        stop_lxc "$current_lxc"
    else
        next_lxc="${LXC_IDS[0]}"
    fi

    # Start the next container
    if [ -n "$next_lxc" ]; then
        start_lxc "$next_lxc"
    fi

    log_message "Rotation complete. Sleeping for $ROTATION_INTERVAL seconds."
    sleep "$ROTATION_INTERVAL"
done