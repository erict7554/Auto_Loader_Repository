import sys
import time

ACTIVATION_DELAY = 30 # Delay between sensor detectioon need for plastic and filling action
EXTRA_FILL_TIME = 5  # seconds to wait after sensor triggers
TIMEOUT = 30         # seconds


def read_cap_sensor():
    # Replace with actual sensor reading logic
    return # sensor state  

def send_error_to_ui(message):
    # Replace with actual UI error handling
    print(f"ERROR: {message}")

start_time = time.time()
cap_sensor_triggered = False

while time.time() - start_time < TIMEOUT:
    if read_cap_sensor():
        cap_sensor_triggered = True
        break
    time.sleep(0.1)  # Polling delay

if cap_sensor_triggered:
    time.sleep(EXTRA_FILL_TIME)
    # Turn relay off
else:
    # Timeout: turn relay off
    send_error_to_ui("Auto Loader Malfunction!")
    print("Auto Loader Malfunction!")