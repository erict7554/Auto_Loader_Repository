import time
import sys
from gpiozero import DigitalInputDevice, DigitalOutputDevice

CAP_SENSOR_PIN = 17   # GPIO pin for capacitive sensor
RELAY_PIN = 26        # GPIO pin for relay

cap_sensor = DigitalInputDevice(CAP_SENSOR_PIN, pull_up=False)
relay = DigitalOutputDevice(RELAY_PIN, active_high=True, initial_value=False)

try:
    ACTIVATION_DELAY = int(sys.argv[1])
    EXTRA_FILL_TIME = int(sys.argv[2])
    TIMEOUT = int(sys.argv[3])
    print(f"Using provided values: ACTIVATION_DELAY={ACTIVATION_DELAY}, EXTRA_FILL_TIME={EXTRA_FILL_TIME}, TIMEOUT={TIMEOUT}")
except (IndexError, ValueError):
    # Handle cases where arguments are missing or not valid integers
    print("Usage: python Auto_Loader_Base_Logic.py <activation_delay> <extra_fill_time> <timeout>")
    # Set default values or exit if arguments are critical
    ACTIVATION_DELAY = 20
    EXTRA_FILL_TIME = 2
    TIMEOUT = 40
    print(f"Using default values: ACTIVATION_DELAY={ACTIVATION_DELAY}, EXTRA_FILL_TIME={EXTRA_FILL_TIME}, TIMEOUT={TIMEOUT}")

def read_cap_sensor():
    needy = cap_sensor.value  # True = HIGH
    return needy, time.time()

def send_error_to_ui(message):
    print(f"ERROR: {message}")
     
def relay_on():
    relay.on()
    print("Relay ON")

def relay_off():
    relay.off()
    print("Relay OFF")

activation_spacing = ACTIVATION_DELAY + EXTRA_FILL_TIME + 10  # Adding a buffer to ensure the sensor is not triggered too frequently
previous_fill_time = -activation_spacing  # Initialize to a negative value to ensure the first fill can occur immediately

try:
    while True:
        [needy, read_time] = read_cap_sensor()

        if needy and (read_time - previous_fill_time) >= activation_spacing:
            print("Filling needed, activating relay...")
            previous_fill_time = read_time
            filled = False

            time.sleep(ACTIVATION_DELAY)
            relay_on()

            start_time = time.time()
            while time.time() - start_time < TIMEOUT:
                [needy, read_time] = read_cap_sensor()
                if not needy:
                    filled = True
                    break
                time.sleep(0.50)

            if filled:
                time.sleep(EXTRA_FILL_TIME)
                relay_off()
            else:
                relay_off()
                send_error_to_ui("Auto Loader Malfunction!")
                print("Auto Loader Malfunction!")
                sys.exit(1)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    relay_off()          # fail-safe: valve closed
    relay.close()
    cap_sensor.close()