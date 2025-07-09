#!/bin/bash

# $1 will contain the single string of space-separated parameters
# Use 'read -r -a' to split this string into an array called params_array
read -r -a params_array <<< "$1"

# Assign individual parameters from the array
ACTIVATION_DELAY=${params_array[0]}
EXTRA_FILL_TIME=${params_array[1]}
TIMEOUT=${params_array[2]}

# For debugging, print the received parameters
echo "Received parameters: ACTIVATION_DELAY=${ACTIVATION_DELAY}, EXTRA_FILL_TIME=${EXTRA_FILL_TIME}, TIMEOUT=${TIMEOUT}"

# Kill any existing instances of the script
pkill -f "Auto_Loader_Base_Logic.py"

# Start your Python program with the parsed parameters
# Ensure the absolute path to your Python script is correct
sudo python3 /home/pi/klipper/Auto_Loader_Repository/auto_loader_start.sh "${ACTIVATION_DELAY}" "${EXTRA_FILL_TIME}" "${TIMEOUT}" &

exit 0