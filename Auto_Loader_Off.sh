#!/bin/bash

PID=$(pgrep -f Auto_Loader_Base_Logic.py)

if [ -z "$PID" ]; then
    echo "No running instance of Auto_Loader_Base_Logic.py found."
else
    kill "$PID"
    echo "Stopped Auto_Loader_Base_Logic.py with PID $PID."
fi