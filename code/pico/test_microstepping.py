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

# Define microstepping modes and required steps per revolution
microstep_modes = {
    "Full Step": (0, 0, 0, 200),       # 200 steps per revolution
    "Half Step": (1, 0, 0, 400),       # 400 steps per revolution
    "Quarter Step": (0, 1, 0, 800),    # 800 steps per revolution
    "Eighth Step": (1, 1, 0, 1600),    # 1600 steps per revolution
    "Sixteenth Step": (1, 1, 1, 3200)  # 3200 steps per revolution
}

# Set microstepping mode for both yaw and pitch
def set_microstep_mode(ms1_pin, ms2_pin, ms3_pin, ms1, ms2, ms3):
    ms1_pin.value(ms1)
    ms2_pin.value(ms2)
    ms3_pin.value(ms3)

# Function to test a microstepping mode on both yaw and pitch
def test_microstepping_mode(name, yaw_pins, pitch_pins, steps, delay):
    print(f"Testing {name} mode")

    # Set microstepping mode for yaw
    set_microstep_mode(yaw_pins['ms1'], yaw_pins['ms2'], yaw_pins['ms3'], *microstep_modes[name][:3])
    # Set microstepping mode for pitch
    set_microstep_mode(pitch_pins['ms1'], pitch_pins['ms2'], pitch_pins['ms3'], *microstep_modes[name][:3])

    # Step both motors for one full revolution
    for _ in range(steps):
        yaw_pins['step'].value(1)
        pitch_pins['step'].value(1)
        time.sleep(delay)
        yaw_pins['step'].value(0)
        pitch_pins['step'].value(0)
        time.sleep(delay)
    
    time.sleep(1)  # Pause between modes

# Define pin dictionaries for yaw and pitch
yaw_pins = {
    'step': yaw_step,
    'dir': yaw_dir,
    'ms1': yaw_ms1,
    'ms2': yaw_ms2,
    'ms3': yaw_ms3,
    'enable': yaw_enable
}

pitch_pins = {
    'step': pitch_step,
    'dir': pitch_dir,
    'ms1': pitch_ms1,
    'ms2': pitch_ms2,
    'ms3': pitch_ms3,
    'enable': pitch_enable
}

# Test each microstepping mode on both drivers
try:
    while True:
        for mode_name, mode_data in microstep_modes.items():
            steps_for_revolution = mode_data[3]
            test_microstepping_mode(mode_name, yaw_pins, pitch_pins, steps=steps_for_revolution, delay=0.005)

except KeyboardInterrupt:
    print("Test interrupted, disabling motors")
    yaw_enable.value(1)  # Disable yaw motor
    pitch_enable.value(1)  # Disable pitch motor  
