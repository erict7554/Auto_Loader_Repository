import time
import requests
import sys

try:
    ACTIVATION_DELAY = int(sys.argv[1])
    EXTRA_FILL_TIME = int(sys.argv[2])
    TIMEOUT = int(sys.argv[3])
    print(f"Using provided values: ACTIVATION_DELAY={ACTIVATION_DELAY}, EXTRA_FILL_TIME={EXTRA_FILL_TIME}, TIMEOUT={TIMEOUT}")
except (IndexError, ValueError):
    # Handle cases where arguments are missing or not valid integers
    print("Usage: python Auto_Loader_Base_Logic.py <activation_delay> <extra_fill_time> <timeout>")
    # Set default values or exit if arguments are critical
    ACTIVATION_DELAY = 10
    EXTRA_FILL_TIME = 2
    TIMEOUT = 30
    print(f"Using default values: ACTIVATION_DELAY={ACTIVATION_DELAY}, EXTRA_FILL_TIME={EXTRA_FILL_TIME}, TIMEOUT={TIMEOUT}")

url_capSense = 'http://192.168.1.67/printer/objects/query?gcode_button%20cap_sense'
url_relay_on = "http://192.168.1.67/printer/gcode/script?script=relay_switch_on"
url_relay_off = "http://192.168.1.67/printer/gcode/script?script=relay_switch_off" 

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
            print("Filling needed, activating relay...")
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
                sys.exit(1)
        
    time.sleep(0.250)  # Polling delay
    
    
        
        

    