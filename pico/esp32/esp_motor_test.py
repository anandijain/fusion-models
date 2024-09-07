import machine
import time
import network
import socket

# Motor class to encapsulate motor control logic
class Motor:
    def __init__(self, step_pin, dir_pin):
        self.step_pin = machine.Pin(step_pin, machine.Pin.OUT)
        self.dir_pin = machine.Pin(dir_pin, machine.Pin.OUT)
    
    def set_direction(self, clockwise=True):
        if clockwise:
            self.dir_pin.value(1)
            print("Motor on DIR pin {} set to CLOCKWISE".format(self.dir_pin))
        else:
            self.dir_pin.value(0)
            print("Motor on DIR pin {} set to COUNTERCLOCKWISE".format(self.dir_pin))
    
    def move_steps(self, steps, delay=850):
        print("Starting to move {} steps with delay {}µs".format(steps, delay))
        for step in range(steps):
            self.step_pin.value(1)
            time.sleep_us(delay)
            self.step_pin.value(0)
            time.sleep_us(delay)
            if step % 50 == 0:
                print("Moved {} steps".format(step))
        print("Finished moving {} steps".format(steps))


m = Motor(step_pin=19, dir_pin=21)
m2 = Motor(step_pin=22, dir_pin=23)

# m.set_direction(clockwise=True)
# m.move_steps(1000, delay=850)
m2.set_direction(clockwise=False)
m2.move_steps(200, delay=1000)
