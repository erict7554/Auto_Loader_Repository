#!/bin/bash

PID=$(pgrep -f Auto_Loader_Base_Logic.py)

if [ -z "$PID" ]; then
    echo "No running instance of duty_cycle.py found."
else
    kill "$PID"
    echo "Stopped duty_cycle.py with PID $PID."
fi