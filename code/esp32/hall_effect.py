import machine
import time

# Define the pin for the Hall effect sensor (D4 is GPIO 4 on the ESP32)
hall_pin = machine.Pin(4, machine.Pin.IN)

# Previous state of the sensor
previous_state = hall_pin.value()

while True:
    current_state = hall_pin.value()  # Read the current state of the sensor

    # Check if the state has changed (from HIGH to LOW or LOW to HIGH)
    if current_state != previous_state:
        # If it changed, print the new state
        if current_state == 0:
            print("Magnet detected (LOW)")
        else:
            print("No magnet (HIGH)")
        
        # Update the previous state to the current state
        previous_state = current_state

    # Small delay to avoid busy-waiting (optional)
    time.sleep(0.05)  # 50 milliseconds
