from machine import Pin, I2C
import time

# AS5600 specific
AS5600_ADDRESS = const(0x36)   # AS5600 has a fixed address
ANGLE_H = const(0x0E)          # Angle register (high byte)
ANGLE_L = const(0x0F)          # Angle register (low byte)

# buf = bytearray(2)             # Preallocate buffer

def getnReg(reg, n):
    i2c.writeto(AS5600_ADDRESS, bytearray([reg]))
    x = i2c.readfrom(AS5600_ADDRESS, n)
    return x

def getAngle():
    buf = getnReg(ANGLE_H, 2)
    return ((buf[0] << 8) | buf[1]) / 4096.0 * 360

# Initialize I2C with a higher frequency for speed
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)  # 400kHz for faster I2C
time.sleep(0.1)  # delay to allow sensor setup

# Measure sample rate
start_time = time.time()
sample_count = 0
duration = 5  # Measure over 5 seconds

while (time.time() - start_time) < duration:
    a = getAngle()  # Perform reading
    print(a)
    sample_count += 1

elapsed_time = time.time() - start_time
samples_per_second = sample_count / elapsed_time

print(f"Samples per second: {samples_per_second:.2f}")
