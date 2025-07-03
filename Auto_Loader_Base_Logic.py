import time
import requests
import sys

ACTIVATION_DELAY = 10  # Delay between sensor detectioon need for plastic and filling action
EXTRA_FILL_TIME = 2 #  seconds to wait after sensor triggers
TIMEOUT = 30 # time until eductor turns off if no sensor trigger

url_capSense = 'http://192.168.1.68/printer/objects/query?gcode_button%20cap_sense'
url_relay_on = "http://192.168.1.68/printer/gcode/script?script=relay_switch_on"
url_relay_off = "http://192.168.1.68/printer/gcode/script?script=relay_switch_off" 

def read_cap_sensor():
    contents = requests.get(url_capSense)
    data = contents.json()
    sensor_state = data["result"]["status"]["gcode_button cap_sense"]["state"]
    needy = sensor_state != "PRESSED"
    read_time = data["result"].get("eventtime", None)
    return needy, read_time

def send_error_to_ui(message):
    # Replace with actual UI error handling
    print(f"ERROR: {message}")

def post_gcode(url_input):
    try:
        response = requests.post(url_input)
        if response.status_code == 200:
            print("Successfully turned on relay.")
        else:
            print(f"Failed to turn on relay")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

activation_spacing = ACTIVATION_DELAY + EXTRA_FILL_TIME + 10  # Adding a buffer to ensure the sensor is not triggered too frequently
previous_fill_time = -activation_spacing  # Initialize to a negative value to ensure the first fill can occur immediately

while True:
    [needy, read_time] = read_cap_sensor()
    if needy == True and (read_time - previous_fill_time) >= activation_spacing:
            previous_fill_time = read_time
            filled = False
            time.sleep(ACTIVATION_DELAY)
            post_gcode(url_relay_on)
            start_time = time.time()
            while time.time() - start_time < TIMEOUT:
                [needy, read_time] = read_cap_sensor()
                if needy == False:
                    filled = True
                    break
                time.sleep(0.250)
            
            if filled == True:
                time.sleep(EXTRA_FILL_TIME) # Wait to fill past sensor indicates filled
                post_gcode(url_relay_off)  # Turn relay off
            else:
                post_gcode(url_relay_off) 
                send_error_to_ui("Auto Loader Malfunction!")
                print("Auto Loader Malfunction!")
        
    time.sleep(0.250)  # Polling delay
    
    
        
        

    