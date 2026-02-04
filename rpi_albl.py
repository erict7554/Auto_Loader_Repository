import time
import sys
import RPi.GPIO as GPIO

CAP_SENSOR_PIN = 17   # GPIO pin for capacitive sensor
RELAY_PIN = 18        # GPIO pin for relay

RELAY_ON = True
RELAY_OFF = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(CAP_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN, GPIO.OUT)

GPIO.output(RELAY_PIN, GPIO.LOW)  # ensure relay off at startup

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
    """
    Reads capacitive sensor state.
    Returns:
        needy (bool): True if fill is needed
        read_time (float): current timestamp
    """
    sensor_state = GPIO.input(CAP_SENSOR_PIN)

    # Adjust logic if your sensor is inverted
    # Here: LOW = material present, HIGH = empty
    needy = sensor_state == GPIO.HIGH

    read_time = time.time()
    return needy, read_time

def send_error_to_ui(message):
    print(f"ERROR: {message}")
     
def relay(command):
    """
    Controls relay state.
    command: RELAY_ON or RELAY_OFF
    """
    if command == RELAY_ON:
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Relay ON")
    elif command == RELAY_OFF:
        GPIO.output(RELAY_PIN, GPIO.LOW)
        print("Relay OFF")
    else:
        raise ValueError("Invalid relay command")

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
            relay(RELAY_ON)

            start_time = time.time()
            while time.time() - start_time < TIMEOUT:
                [needy, read_time] = read_cap_sensor()
                if not needy:
                    filled = True
                    break
                time.sleep(0.50)

            if filled:
                time.sleep(EXTRA_FILL_TIME)
                relay(RELAY_OFF)
            else:
                relay(RELAY_OFF)
                send_error_to_ui("Auto Loader Malfunction!")
                print("Auto Loader Malfunction!")
                sys.exit(1)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    relay(RELAY_OFF)   # fail-safe: valve closed
    GPIO.cleanup()
    print("GPIO cleaned up")