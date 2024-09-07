from machine import Pin, PWM
import time

# Define the motor control pins
in1 = Pin(3, Pin.OUT)
in2 = Pin(4, Pin.OUT)

# Define the PWM pin for speed control (assuming Enable is connected to GP5)
enable = PWM(Pin(2))  # Replace 5 with the correct GPIO number for Enable

# Set the PWM frequency (typically between 1kHz to 10kHz for motor control)
enable.freq(1000)  # 1 kHz

# Function to set the motor forward with a specified speed
def motor_forward(speed_percentage):
    in1.value(1)  # Set IN1 high to move forward
    in2.value(0)  # Set IN2 low
    duty_cycle = int((speed_percentage / 100) * 65535)  # Convert percentage to duty cycle
    enable.duty_u16(duty_cycle)  # Set PWM duty cycle

def stop_motor():
    enable.duty_u16(0)  # Set PWM duty to 0 to stop the motor
    in1.value(0)
    in2.value(0)

        
while True:        
    # Set the motor to move forward at 10% speed
    motor_forward(100)  # 10% speed
    print("Motor running forward at 10% speed")

    # Run for 5 seconds, then stop
    time.sleep(5)

    # Function to stop the motor

    stop_motor()
    time.sleep(5)
    print("Motor stopped")
