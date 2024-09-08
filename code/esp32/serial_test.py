from machine import Pin
import sys
import time

# Initialize the LED pin (Onboard LED on ESP32 usually on GPIO 2)
led = Pin(2, Pin.OUT)

# Turn off LED initially
led.value(1)
print("hello")

# Function to process serial input
def handle_input(input_str):
    input_str = input_str.strip().upper()  # Clean and normalize input
    print(input_str)
    if input_str == "ON":
        led.value(1)  # Turn on LED
        print("LED is ON")
    elif input_str == "OFF":
        led.value(0)  # Turn off LED
        print("LED is OFF")
    else:
        print("Unknown command")

# Main loop to read serial input
while True:
#     if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
#         input_data = sys.stdin.read()  # Read the serial input
#         handle_input(input_data)  # Process the input
    data = sys.stdin.readline()
    print(data)
    if data == "N":
        led.on()
    elif data == "F":
        led.off()

    time.sleep(0.1)  # Small delay to avoid CPU overuse
