from machine import Pin, PWM
from time import sleep

# Initialize the PWM on GPIO 34 (D34)
esc = PWM(Pin(34), freq=50)  # 50Hz PWM frequency for the ESC

# Function to set throttle
def set_throttle(throttle):
    # throttle should be between 0 and 100 (0 = 1ms, 100 = 2ms)
    # Convert throttle to duty cycle (range 40-115 for most ESCs)
    duty = int(40 + (throttle / 100) * (115 - 40))
    esc.duty(duty)

try:
    while True:
        # Example: Ramp up throttle
        for throttle in range(0, 101, 5):
            print("Throttle: ", throttle, "%")
            set_throttle(throttle)
            sleep(1)

        # Hold at max throttle for 2 seconds
        sleep(2)

        # Ramp down throttle
        for throttle in range(100, -1, -5):
            print("Throttle: ", throttle, "%")
            set_throttle(throttle)
            sleep(1)
            
        # Hold at zero throttle for 2 seconds
        sleep(2)

except KeyboardInterrupt:
    # Stop the motor when the loop ends
    set_throttle(0)
    esc.deinit()  # Deinitialize PWM
