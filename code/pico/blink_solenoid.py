import machine
import time

# Initialize GP9 as an output pin
led = machine.Pin(9, machine.Pin.OUT)

while True:
    led.value(1)   # Turn the LED on
    time.sleep(1)  # Wait for 100ms
    led.value(0)   # Turn the LED off
    time.sleep(1)    # Wait for 1 second
