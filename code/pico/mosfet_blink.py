from machine import Pin
import time

# Define the GPIO pin connected to the MOSFET gate
mosfet_gate = Pin(16, Pin.OUT)  # GP15

while True:
    mosfet_gate.value(1)  # Turn LED on
    time.sleep(.2)          # Wait for 1 second
    mosfet_gate.value(0)  # Turn LED off
    time.sleep(1)          # Wait for 1 second
