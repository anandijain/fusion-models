from machine import Pin, I2C
from time import ticks_us, ticks_diff

# AS5600 specific constants
AS5600_ADDRESS = 0x36   # AS5600 I2C address
ANGLE_H = 0x0E          # Angle register (high byte)

# Preallocate buffer
buf = bytearray(2)

# I2C initialization
i2c = I2C(0, scl=Pin(5), sda=Pin(4))

# Function to read from AS5600
def getnReg(reg, n):
    i2c.writeto(AS5600_ADDRESS, bytearray([reg]))
    i2c.readfrom_into(AS5600_ADDRESS, buf)
    return buf

# Function to get the current angle in degrees
def getAngle():
    buf = getnReg(ANGLE_H, 2)
    angle_raw = (buf[0] << 8) | buf[1]
    angle_deg = (angle_raw / 4096.0) * 360.0  # Convert to degrees
    return angle_deg

# Number of readings for the moving average
WINDOW_SIZE = 100

# Circular buffer for angles and times
angles = [0] * WINDOW_SIZE
times = [0] * WINDOW_SIZE

# Initialize readings
for i in range(WINDOW_SIZE):
    angles[i] = getAngle()
    times[i] = ticks_us()

# Function to compute the RPM using multiple readings
def compute_rpm(angles, times, window_size):
    total_angle_diff = 0
    total_time_diff = 0

    # Iterate over the window to sum up angle differences and time differences
    for i in range(1, window_size):
        # angle_diff = angles[i - 1] - angles[i]
        # if angle_diff < 0:  # Handle angle wrapping (0 to 360)
        #     angle_diff += 360
        if angles[i] > angles[i - 1]:
            angle_diff = angles[i-1] + (360 - angles[i])
        else: 
            angle_diff = angles[i-1] - angles[i]
           
        time_diff = ticks_diff(times[i], times[i - 1]) / 1_000_000.0  # Convert time to seconds
        
        total_angle_diff += angle_diff
        total_time_diff += time_diff

    # Calculate average angular velocity (degrees per second)
    avg_deg_per_sec = total_angle_diff / total_time_diff if total_time_diff > 0 else 0

    # Convert angular velocity to RPM
    rpm = avg_deg_per_sec / 6.0  # 360 degrees per revolution, 60 seconds in a minute
    return rpm

# Start reading and computing RPM
try:
    sample_index = 0
    while True:
        # Get current angle and timestamp
        angles[sample_index] = getAngle()
        times[sample_index] = ticks_us()

        # Move to the next index in the circular buffer
        sample_index = (sample_index + 1) % WINDOW_SIZE

        # Compute RPM using the moving average
        if sample_index == 0:  # Start calculating RPM only when the buffer is full
            rpm = compute_rpm(angles, times, WINDOW_SIZE)
            print("RPM: {:.2f}".format(rpm))

except KeyboardInterrupt:
    print("Interrupted")
