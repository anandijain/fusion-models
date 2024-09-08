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

    def forward(self, speed_percentage):
        """Move the motor forward with the specified speed percentage (0-100)."""
        self.in1.value(1)
        self.in2.value(0)
        duty_cycle = int((speed_percentage / 100) * 65535)  # Convert percentage to duty cycle
        self.enable.duty_u16(duty_cycle)

    def reverse(self, speed_percentage):
        """Move the motor in reverse with the specified speed percentage (0-100)."""
        self.in1.value(0)
        self.in2.value(1)
        duty_cycle = int((speed_percentage / 100) * 65535)  # Convert percentage to duty cycle
        self.enable.duty_u16(duty_cycle)

    def stop(self):
        """Stop the motor."""
        self.enable.duty_u16(0)
        self.in1.value(0)
        self.in2.value(0)

# Example usage for two motors:
motor1 = Motor(enable_pin=2, in1_pin=3, in2_pin=4)
motor2 = Motor(enable_pin=5, in1_pin=6, in2_pin=7)

while True:
    # Control motor1 and motor2
    motor1.reverse(70)  # Move motor1 forward at 50% speed
    motor2.forward(70)  # Move motor2 in reverse at 75% speed

    time.sleep(5)       # Run for 5 seconds
    motor1.stop()       # Stop motor1
    motor2.stop()       # Stop motor2
    time.sleep(5)       # Run for 5 seconds
