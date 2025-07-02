import RPi.GPIO as GPIO
import time
print('Changes made to Auto_Loader_Base_Logic.py 2')
# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin 17 as an output
GPIO.setup(17, GPIO.OUT)

while True:
    GPIO.output(17, GPIO.HIGH)  # Turn on
    time.sleep(5)
    GPIO.output(17, GPIO.LOW)   # Turn off
    time.sleep(5)
