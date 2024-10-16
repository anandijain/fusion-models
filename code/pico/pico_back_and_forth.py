from machine import Pin
import time

# Define pin numbers
# pulPin = Pin(18, Pin.OUT)  # Pulse pin connected to PUL- on DM542T
# dirPin = Pin(19, Pin.OUT)  # Direction pin connected to DIR- on DM542T
pulPin = Pin(17, Pin.OUT)  # Pulse pin connected to PUL- on DM542T
dirPin = Pin(16, Pin.OUT)  # Direction pin connected to DIR- on DM542T

# Define constants
stepsPerRevolution = 200   # Assuming 1.8 degrees per step (200 steps for 360 degrees)
delayTime = 1500  # Delay between steps (microseconds)

def step_motor(direction):
    dirPin.value(direction)  # Set direction
    for _ in range(stepsPerRevolution):
        pulPin.value(1)
        time.sleep_us(delayTime)
        pulPin.value(0)
        time.sleep_us(delayTime)

while True:
    # Rotate forward
    step_motor(1)
    time.sleep(1)  # Pause between direction changes

    # Rotate backward
    step_motor(0)
    time.sleep(1)  # Pause before repeating
