from machine import Pin
import time

# Define the LED pin (onboard LED is usually on pin 25)
led = Pin("LED", Pin.OUT)

# Blink the LED
while True:
    led.on()   # Turn the LED on
    time.sleep(1)  # Wait for 1 second
    led.off()  # Turn the LED off
    time.sleep(1)  # Wait for 1 second
