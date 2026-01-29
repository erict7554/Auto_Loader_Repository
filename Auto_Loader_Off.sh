#!/bin/bash

PID=$(pgrep -f rpi_albl.py)

if [ -z "$PID" ]; then
    echo "No running instance of rpi_albl.py found."
else
    kill "$PID"
    echo "Stopped rpi_albl.py with PID $PID."
fi