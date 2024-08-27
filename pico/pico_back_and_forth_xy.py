import machine
import time

# Motor class to encapsulate motor control logic
class Motor:
    def __init__(self, step_pin, dir_pin):
        self.step_pin = machine.Pin(step_pin, machine.Pin.OUT)
        self.dir_pin = machine.Pin(dir_pin, machine.Pin.OUT)
    
    def set_direction(self, clockwise=True):
        if clockwise:
            self.dir_pin.value(1)
        else:
            self.dir_pin.value(0)
    
    def move_steps(self, steps, delay=0.001):
        for _ in range(steps):
            self.step_pin.value(1)
            time.sleep(delay)
            self.step_pin.value(0)
            time.sleep(delay)

# Instantiate two motors
motor_yaw = Motor(step_pin=16, dir_pin=17)
motor_pitch = Motor(step_pin=18, dir_pin=19)

# Main loop to control the motors
while True:
    # Control yaw motor
    motor_yaw.set_direction(clockwise=True)
    motor_yaw.move_steps(200)
    time.sleep(1)
    
    motor_yaw.set_direction(clockwise=False)
    motor_yaw.move_steps(200)
    time.sleep(1)
    
    # Control pitch motor
    motor_pitch.set_direction(clockwise=True)
    motor_pitch.move_steps(200)
    time.sleep(1)
    
    motor_pitch.set_direction(clockwise=False)
    motor_pitch.move_steps(200)
    time.sleep(1)

