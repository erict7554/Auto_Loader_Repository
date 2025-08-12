#!/bin/bash
# Stop all running instances of the auto_loader@… service

# Get the list of running instances
INSTANCES=$(sudo systemctl list-units --type=service --state=running | grep -oP 'auto_loader@[\d:]+\.service')

if [ -z "$INSTANCES" ]; then
    echo "No Auto Loader instances found"
else
    echo "Stopping Auto Loader instances..."
    while read -r svc; do
        echo "Stopping $svc"
        sudo systemctl stop "$svc"
    done <<< "$INSTANCES"
fi