from machine import Pin, I2C
from time import sleep
import time 

# AS5600 specific
AS5600_ADDRESS = const(0x36)   # AS5600 has a fixed address (so can only use one per I2C bus?)
ANGLE_H	= const(0x0E)          # Angle register (high byte)
ANGLE_L	= const(0x0F)          # Angle register (low byte)

def getnReg(reg, n):
    i2c.writeto(AS5600_ADDRESS, bytearray([reg]))
    t =	i2c.readfrom(AS5600_ADDRESS, n)
    return t    


def getAngle():
    buf = getnReg(ANGLE_H, 2)
    return ((buf[0]<<8) | buf[1])/ 4096.0*360

i2c = I2C(0,scl=Pin(5), sda=Pin(4))
time.sleep(0.1)  # delay 1ms

while True:
    print(getAngle())
