from machine import Pin
import sys
import time

# Initialize the LED pin (Onboard LED on ESP32 usually on GPIO 2)
led = Pin(2, Pin.OUT)

# Turn off LED initially
led.value(0)

# Main loop to read serial input
while True:
    data = sys.stdin.readline().strip()
    print("ECHO: {}".format(data))
    if data == "ON":
        led.on()
    elif data == "OFF":
        led.off()
    time.sleep(0.1)  # Small delay to avoid CPU overuse
