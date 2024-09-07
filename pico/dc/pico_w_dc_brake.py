from machine import Pin
import time

# Define the motor control pins
en1 = Pin(2, Pin.OUT)
in1 = Pin(3, Pin.OUT)
in2 = Pin(4, Pin.OUT)


en2 = Pin(2, Pin.OUT)
in3 = Pin(3, Pin.OUT)
in4 = Pin(4, Pin.OUT)

# Function to lock (brake) the motor
def brake_motor():
    in1.value(0)  # Set both IN1 and IN2 to low
    in2.value(0)

def fwd_motor():
    in1.value(1)  # Set both IN1 and IN2 to low
    in2.value(0)


en.value(1)
# Example usage: lock the motor for 5 seconds, then release
while True:

    fwd_motor()
    print("Motor is locked (braked)")
    time.sleep(5)

    # Release the motor (optional, sets both pins high)
    in1.value(1)
    in2.value(1)
    print("Motor is released")
    time.sleep(5)
