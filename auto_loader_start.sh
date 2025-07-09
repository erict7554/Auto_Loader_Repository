#!/bin/bash

# For debugging, print the received parameters
echo "Received parameters: ACTIVATION_DELAY=$1, EXTRA_FILL_TIME=$2, TIMEOUT=$3"

# Kill any existing instances of the script
pkill -f "Auto_Loader_Base_Logic.py"

# Start your Python program with the parsed parameters
# Ensure the absolute path to your Python script is correct

sudo python /home/pi/klipper/Auto_Loader_Repository/Auto_Loader_Base_Logic.py $1 $2 $3 &

exit 0