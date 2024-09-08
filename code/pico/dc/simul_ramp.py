from machine import Pin, PWM
import time

class Motor:
    def __init__(self, enable_pin, in1_pin, in2_pin, pwm_freq=1000):
        # Initialize pins
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        
        # Initialize PWM for speed control
        self.enable = PWM(Pin(enable_pin))
        self.enable.freq(pwm_freq)  # Set PWM frequency
        self.current_speed = 0  # Track the current speed

    def forward(self, speed_percentage):
        """Move the motor forward with the specified speed percentage (0-100)."""
        self.in1.value(1)
        self.in2.value(0)
        duty_cycle = int((speed_percentage / 100) * 65535)  # Convert percentage to duty cycle
        self.enable.duty_u16(duty_cycle)
        self.current_speed = speed_percentage

    def reverse(self, speed_percentage):
        """Move the motor in reverse with the specified speed percentage (0-100)."""
        self.in1.value(0)
        self.in2.value(1)
        duty_cycle = int((speed_percentage / 100) * 65535)  # Convert percentage to duty cycle
        self.enable.duty_u16(duty_cycle)
        self.current_speed = speed_percentage

    def stop(self):
        """Stop the motor."""
        self.enable.duty_u16(0)
        self.in1.value(0)
        self.in2.value(0)
        self.current_speed = 0

def ramp_up_simultaneously(motors, target_speeds, directions, ramp_time):
    """Gradually ramp up multiple motors to target speeds over ramp_time with specific directions."""
    step_time = 0.1  # Time between each speed increment in seconds
    steps = int(ramp_time / step_time)
    speed_steps = [target_speed / steps for target_speed in target_speeds]
    
    # Initialize current speeds for each motor
    current_speeds = [0] * len(motors)
    
    for _ in range(steps):
        for i, motor in enumerate(motors):
            if current_speeds[i] < target_speeds[i]:
                current_speeds[i] += speed_steps[i]
                if current_speeds[i] > target_speeds[i]:
                    current_speeds[i] = target_speeds[i]
                
                # Set motor direction and speed based on the direction specified
                if directions[i] == "forward":
                    motor.forward(current_speeds[i])
                elif directions[i] == "reverse":
                    motor.reverse(current_speeds[i])
                
        time.sleep(step_time)
    
    # Set the final speeds for all motors
    for i, motor in enumerate(motors):
        if directions[i] == "forward":
            motor.forward(target_speeds[i])
        elif directions[i] == "reverse":
            motor.reverse(target_speeds[i])

# Example usage for two motors:
motor1 = Motor(enable_pin=2, in1_pin=3, in2_pin=4)
motor2 = Motor(enable_pin=5, in1_pin=6, in2_pin=7)

while True:
    # Ramp up both motors to 100% speed over 2 seconds simultaneously
    motors = [motor1, motor2]
    target_speeds = [100, 100]  # Ramp to 100% speed for both motors
    directions = ["forward", "reverse"]  # Motor 2 forward, Motor 1 reverse
    ramp_up_simultaneously(motors, target_speeds, directions, ramp_time=1)

    time.sleep(5)  # Run at full speed for 5 seconds
    motor1.stop()  # Stop motor1
    motor2.stop()  # Stop motor2
    time.sleep(5)  # Pause for 5 seconds
