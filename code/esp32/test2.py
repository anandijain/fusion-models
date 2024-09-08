import select
from machine import Pin
import sys
import time
i = 0 
led = Pin(2, Pin.OUT)

# Turn off LED initially
led.value(0)

while True:
    time.sleep(0.1)
    if select.select([sys.stdin],[],[],0)[0]:
        input_str = sys.stdin.readline().strip()
        if input_str == "ON":
            led.value(1)  # Turn on LED
            print("LED is ON")
        elif input_str == "OFF":
            led.value(0)  # Turn off LED
            print("LED is OFF")
        else:
            print("Unknown command: {}".format(input_str))
