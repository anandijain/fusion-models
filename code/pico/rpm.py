from machine import Pin, I2C
from time import sleep, ticks_ms, ticks_diff, ticks_us

# AS5600 specific constants
AS5600_ADDRESS = 0x36   # AS5600 I2C address
ANGLE_H = 0x0E          # Angle register (high byte)

buf = bytearray(2)  # Preallocate buffer
def getnReg(reg, n):
    i2c.writeto(AS5600_ADDRESS, bytearray([reg]))
    i2c.readfrom_into(AS5600_ADDRESS, buf)
    return buf

def getAngle():
    buf = getnReg(ANGLE_H, 2)
    angle_raw = (buf[0] << 8) | buf[1]
    angle_deg = (angle_raw / 4096.0) * 360.0  # Convert to degrees
    return angle_deg

# Initialize I2C
i2c = I2C(0, scl=Pin(5), sda=Pin(4))

# Initial angle and time
prev_angle = getAngle()
start_time = prev_time = ticks_us()
samples = 0
try: 
    while True:
        # sleep(0.1)  # Sample every 0.1 seconds
        curr_angle = getAngle()
        curr_time = ticks_us()
        
        # Calculate time difference in seconds
        delta_time = ticks_diff(curr_time, prev_time) / 1_000_000.0
        
        if curr_angle < prev_angle:
            delta_angle = curr_angle + 360 - prev_angle
        else:
            delta_angle = curr_angle - prev_angle
        
        # Calculate angular velocity in degrees per second
        deg_per_sec = delta_angle / delta_time
        
        # Calculate RPM (Revolutions Per Minute)
        rpm = deg_per_sec / 6.0  # Since 360 degrees per 60 seconds equals 6 degrees per second per RPM
        
        
        # Update previous angle and time
        prev_angle = curr_angle
        prev_time = curr_time
        samples += 1

except KeyboardInterrupt:
    print("Interrupted")
    # i2c.deinit()
    print("I2C Deinitialized")
    print("RPM: {:.2f}".format(rpm))
    print("Sample count: ", samples)
    print("Elapsed time: ", (ticks_diff(ticks_us(), start_time) / 1_000_000.0), " seconds")
    print("Samples per second: {:.2f}".format(samples / (ticks_diff(ticks_us(), start_time) / 1_000_000.0)))