#!/bin/bash
# Usage: ./auto_loader_start.sh ACTIVATION_DELAY EXTRA_FILL_TIME TIMEOUT

ACTIVATION_DELAY=$1
EXTRA_FILL_TIME=$2
TIMEOUT=$3

# Start the systemd templated service with the parameters
sudo systemctl start "auto_loader@${ACTIVATION_DELAY}:${EXTRA_FILL_TIME}:${TIMEOUT}"