from machine import Pin, PWM, I2C
from time import sleep
import time 


# Initialize the PWM on GPIO 15
# esc = PWM(Pin(14))
# esc.freq(50)  # 50Hz PWM frequency for the ESC
esc2 = PWM(Pin(15))
esc2.freq(50)  # 50Hz PWM frequency for the ESC
sleep(1)
# Function to set throttle
def set_throttle(throttle):
    # throttle should be between 0 and 100 (0% = 1ms pulse, 100% = 2ms pulse)
    pulse_width_ms = 1 + (throttle / 100) * 1  # Calculate pulse width in milliseconds
    duty_u16 = int((pulse_width_ms / 20) * 65535)  # Convert pulse width to duty cycle
    esc2.duty_u16(duty_u16)
    # esc2.duty_u16(duty_u16)

# try:
#     while True:
#         # Example: Ramp up throttle
#         for throttle in range(0, 101, 5):
#             print("Throttle: ", throttle, "%")
#             set_throttle(throttle)
#             sleep(1)

#         # Hold at max throttle for 2 seconds
#         sleep(2)

#         # Ramp down throttle
#         for throttle in range(100, -1, -5):
#             print("Throttle: ", throttle, "%")
#             set_throttle(throttle)
#             sleep(1)
                
#         # Hold at zero throttle for 2 seconds
#         sleep(2)

# except KeyboardInterrupt:
#     # Stop the motor when the loop ends
#     set_throttle(0)
#     esc.deinit()  # Deinitialize PWM

set_throttle(0)
sleep(3)
set_throttle(25)
sleep(0.5)
set_throttle(10)

# AS5600 specific
AS5600_ADDRESS = const(0x36)   # AS5600 has a fixed address (so can only use one per I2C bus?)
ANGLE_H	= const(0x0E)          # Angle register (high byte)
ANGLE_L	= const(0x0F)          # Angle register (low byte)

def getnReg(reg, n):
    i2c.writeto(AS5600_ADDRESS, bytearray([reg]))
    # time.sleep(0.01)  # delay 1ms
    t =	i2c.readfrom(AS5600_ADDRESS, n)
    return t    


def getAngle():
    buf = getnReg(ANGLE_H, 2)
    return ((buf[0]<<8) | buf[1])/ 4096.0*360

i2c = I2C(0,scl=Pin(5), sda=Pin(4))
time.sleep(0.1)  # delay 1ms

while True:
    print(getAngle())
    # sleep(.1)
