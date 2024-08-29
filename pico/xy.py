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
    
    def step(self, delay=850):
        self.step_pin.value(1)
        time.sleep_us(delay)
        self.step_pin.value(0)
        time.sleep_us(delay)

    def move_steps(self, steps, delay=850):
        for _ in range(steps):
            self.step(delay)

# Function to move both motors together
def move_steps_together(motor1, motor2, steps, delay=850):
    for _ in range(steps):
        motor1.step(delay)
        motor2.step(delay)

# Instantiate two motors
motor_yaw = Motor(step_pin=16, dir_pin=17)
motor_pitch = Motor(step_pin=18, dir_pin=19)

# Main loop to control the motors concurrently
steps = 200 * 4  # Number of steps for each motor
delay = 850  # Delay between steps

while True:
    # Move both motors in the clockwise direction
    motor_yaw.set_direction(clockwise=True)
    motor_pitch.set_direction(clockwise=True)
    move_steps_together(motor_yaw, motor_pitch, steps, delay)
    time.sleep(1)
    
    # Move both motors in the counterclockwise direction
    motor_yaw.set_direction(clockwise=False)
    motor_pitch.set_direction(clockwise=False)
    move_steps_together(motor_yaw, motor_pitch, steps, delay)
    time.sleep(1)
