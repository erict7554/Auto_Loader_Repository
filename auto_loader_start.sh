#!/bin/bash

# Parameters passed from Klipper macro
ACTIVATION_DELAY=$1
EXTRA_FILL_TIME=$2
TIMEOUT=$3

# Kill any existing instances of the script
pkill -f "Auto_Loader_Base_Logic.py"

# Start your Python program with the parameters
sudo python3 /home/pi/Auto_Loader_Base_Logic.py "${ACTIVATION_DELAY}" "${EXTRA_FILL_TIME}" "${TIMEOUT}" &

exit 0