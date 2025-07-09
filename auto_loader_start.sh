#!/bin/bash

# Parameters passed individually from Klipper macro
ACTIVATION_DELAY=$1
EXTRA_FILL_TIME=$2
TIMEOUT=$3

# For debugging, print the received parameters (these will appear in Klipper's log if verbose:True)
echo "Received parameters: ACTIVATION_DELAY=${ACTIVATION_DELAY}, EXTRA_FILL_TIME=${EXTRA_FILL_TIME}, TIMEOUT=${TIMEOUT}"

# Kill any existing instances of the Python script to prevent multiple runs
pkill -f "Auto_Loader_Base_Logic.py"

# Start your Python program with the parsed parameters
# IMPORTANT: Ensure the absolute path to your Python script (Auto_Loader_Base_Logic.py) is correct.
sudo python3 /home/pi/klipper/Auto_Loader_Repository/Auto_Loader_Base_Logic.py "${ACTIVATION_DELAY}" "${EXTRA_FILL_TIME}" "${TIMEOUT}" &

exit 0