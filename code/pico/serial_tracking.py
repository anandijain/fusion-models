import sys
import machine
from machine import Pin
import time

class StepperMotor:
    def __init__(self, step_pin, dir_pin):
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
    
    def set_direction(self, clockwise=True):
        if clockwise:
            self.dir_pin.value(1)
        else:
            self.dir_pin.value(0)
    
    def step(self, delay=1500):
        self.step_pin.value(1)
        time.sleep_us(delay)
        self.step_pin.value(0)
        time.sleep_us(delay)

    def move_steps(self, steps, delay=1500):
        for _ in range(steps):
            self.step(delay=delay)

def move_both_motors_simultaneously(yaw_motor, pitch_motor, yaw_steps, pitch_steps, yaw_clockwise, pitch_clockwise):
    yaw_motor.set_direction(clockwise=yaw_clockwise)
    pitch_motor.set_direction(clockwise=pitch_clockwise)

    max_steps = max(yaw_steps, pitch_steps)
    
    yaw_ratio = yaw_steps / max_steps if yaw_steps > 0 else 0
    pitch_ratio = pitch_steps / max_steps if pitch_steps > 0 else 0

    # Adjust this delay to control the speed of movement
    delay = 850

    for step in range(max_steps):
        if step < yaw_steps * yaw_ratio:
            yaw_motor.step(delay)
        if step < pitch_steps * pitch_ratio:
            pitch_motor.step(delay)

def parse_serial_data(data):
    try:
        # Split the input string by commas and parse the key-value pairs
        pairs = data.split(',')
        parsed_data = {}
        for pair in pairs:
            key, value = pair.split('=')
            parsed_data[key.strip()] = value.strip()
        
        # Extract values
        yaw_dir = parsed_data.get('yawDir')
        yaw_steps = int(parsed_data.get('yawSteps'))
        pitch_dir = parsed_data.get('pitchDir')
        pitch_steps = int(parsed_data.get('pitchSteps'))
        delay = int(parsed_data.get('delay'))

        yaw_clockwise = yaw_dir == "clockwise"
        pitch_clockwise = pitch_dir == "clockwise"

        print("Yaw Direction:", yaw_dir)
        print("Yaw Steps:", yaw_steps)
        print("Pitch Direction:", pitch_dir)
        print("Pitch Steps:", pitch_steps)
        
        # Move motors simultaneously
        # move_both_motors_simultaneously(yaw, pitch, yaw_steps, pitch_steps, yaw_clockwise, pitch_clockwise)

        # move separately
        yaw.set_direction(clockwise=yaw_clockwise)
        yaw.move_steps(yaw_steps, delay=delay)
        pitch.set_direction(clockwise=pitch_clockwise)
        pitch.move_steps(pitch_steps, delay=delay)

    except Exception as e:
        print("Failed to parse data:", e)

# Initialize motors
yaw = StepperMotor(step_pin=17, dir_pin=16)
pitch = StepperMotor(step_pin=19, dir_pin=18)

# Main loop

#test msg
# yawDir=clockwise,yawSteps=100,pitchDir=counterclockwise,pitchSteps=100,delay=1500
# yawDir=counterclockwise,yawSteps=100,pitchDir=counterclockwise,pitchSteps=100,delay=1500
while True:
    data = sys.stdin.readline().strip()

    print("Received data:", data)
    parse_serial_data(data)
    
    time.sleep(0.005)
