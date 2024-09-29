from machine import Pin
import time

# Yaw driver pin definitions
yaw_dir = Pin(16, Pin.OUT)
yaw_step = Pin(17, Pin.OUT)
yaw_sleep = Pin(10, Pin.OUT)
yaw_reset = Pin(11, Pin.OUT)
yaw_ms3 = Pin(12, Pin.OUT)
yaw_ms2 = Pin(13, Pin.OUT)
yaw_ms1 = Pin(14, Pin.OUT)
yaw_enable = Pin(15, Pin.OUT)

# Pitch driver pin definitions
pitch_dir = Pin(18, Pin.OUT)
pitch_step = Pin(19, Pin.OUT)
pitch_sleep = Pin(20, Pin.OUT)
pitch_reset = Pin(21, Pin.OUT)
pitch_ms3 = Pin(22, Pin.OUT)
pitch_ms2 = Pin(26, Pin.OUT)
pitch_ms1 = Pin(27, Pin.OUT)
pitch_enable = Pin(28, Pin.OUT)

# Initialize drivers to known states
def initialize_driver(dir_pin, sleep_pin, reset_pin, ms1_pin, ms2_pin, ms3_pin, enable_pin):
    dir_pin.value(0)       # Set direction to 0
    sleep_pin.value(1)     # Keep awake
    reset_pin.value(1)     # Keep reset inactive
    ms1_pin.value(0)       # Set microstep setting
    ms2_pin.value(0)
    ms3_pin.value(0)
    enable_pin.value(0)    # Enable the driver

initialize_driver(yaw_dir, yaw_sleep, yaw_reset, yaw_ms1, yaw_ms2, yaw_ms3, yaw_enable)
initialize_driver(pitch_dir, pitch_sleep, pitch_reset, pitch_ms1, pitch_ms2, pitch_ms3, pitch_enable)

# Test the stepper motors
def test_stepper(step_pin, steps, delay):
    for _ in range(steps):
        step_pin.value(1)
        time.sleep(delay)
        step_pin.value(0)
        time.sleep(delay)

# Test sequence
try:
    while True:
        print("Testing yaw motor")
        test_stepper(yaw_step, 200, 0.01)  # 200 steps for yaw motor
        time.sleep(1)                      # Pause before the next motor

        print("Testing pitch motor")
        test_stepper(pitch_step, 200, 0.01)  # 200 steps for pitch motor
        time.sleep(1)                       # Pause before repeating

except KeyboardInterrupt:
    print("Test interrupted, disabling motors")

# Disable motors when the test is stopped
yaw_enable.value(1)
pitch_enable.value(1)
