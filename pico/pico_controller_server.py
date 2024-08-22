from machine import Pin
import time
import network
import socket

# Define pin numbers
pulPin = Pin(6, Pin.OUT)  # Pulse pin connected to PUL- on DM542T
dirPin = Pin(7, Pin.OUT)  # Direction pin connected to DIR- on DM542T

# Define constants
delayTime = 1000  # Delay between steps (microseconds)

# Connect to Wi-Fi
ssid = 'JAIN'
password = 'sudshome610st'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    print('Connecting to network...')
    time.sleep(1)

print('Connected to Wi-Fi')
print('IP:', wlan.ifconfig()[0])

# Function to step the motor
def step_motor(direction, steps):
    dirPin.value(direction)  # Set direction
    for _ in range(steps):
        pulPin.value(1)
        time.sleep_us(delayTime)
        pulPin.value(0)
        time.sleep_us(delayTime)

# Function to handle HTTP requests
def handle_request(request):
    request = str(request)
    if '/forward' in request:
        try:
            steps = int(request.split('/forward?steps=')[1].split(' ')[0])
            step_motor(1, steps)
            print("got forward")
            print(steps)
            return f'Motor moving forward {steps} steps'
        except:
            return 'Invalid number of steps for forward command'
    elif '/backward' in request:
        try:
            steps = int(request.split('/backward?steps=')[1].split(' ')[0])
            step_motor(0, steps)
            print("got backward")
            print(steps)
            return f'Motor moving backward {steps} steps'
        except:
            return 'Invalid number of steps for backward command'
    else:
        return 'Invalid command'

# Setup a simple web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)
print('Listening on', addr)

while True:
    conn, addr = server.accept()
    print('Connection from', addr)
    request = conn.recv(1024)
    response = handle_request(request)
    
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/plain\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
