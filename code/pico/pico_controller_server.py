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

# Instantiate motors for yaw and pitch
motor_yaw = Motor(step_pin=16, dir_pin=17)
motor_pitch = Motor(step_pin=18, dir_pin=19)

# Define constants
delay_time = 1000  # Delay between steps (microseconds)

# Connect to Wi-Fi
ssid = 'JAIN'
password = 'sudshome610st'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    print('Connecting to network...')
    time.sleep(1)

print('Connected to Wi-Fi')
print('IP:', wlan.ifconfig()[0])

def handle_request(request):
    request = request.decode('utf-8')  # Decode the request from bytes to string
    print("\n--- New Request Received ---")
    print("Full request:", request)
    
    # Split request into lines and get the request line (first line)
    request_lines = request.split('\r\n')
    if len(request_lines) < 1:
        print("No request line found")
        return 'Invalid command'
    
    request_line = request_lines[0]
    print("Request line:", request_line)
    
    # Split request line into method, path, and protocol
    parts = request_line.split(' ')
    if len(parts) < 3:
        print("Invalid request line format")
        return 'Invalid command'
    
    method, path_query, protocol = parts[0], parts[1], parts[2]
    print("Method: {}, Path+Query: {}, Protocol: {}".format(method, path_query, protocol))
    
    if not path_query.startswith('/control'):
        print("Path does not start with /control")
        return 'Invalid command'
    
    # Check if there is a query string
    if '?' in path_query:
        path, query_string = path_query.split('?', 1)
        print("Path:", path)
        print("Query string:", query_string)
    else:
        query_string = ''
        print("No query string found")
    
    # Parse query parameters
    params = {}
    if query_string:
        pairs = query_string.split('&')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value
                print("Parameter parsed: {} = {}".format(key, value))
            else:
                print("Invalid parameter format: {}".format(pair))
    
    # Required parameters
    required_params = ['yaw_dir', 'yaw_steps', 'pitch_dir', 'pitch_steps']
    missing_params = [param for param in required_params if param not in params]
    if missing_params:
        print("Missing parameters: {}".format(missing_params))
        return 'Invalid command'
    
    try:
        # Parse yaw direction and steps
        yaw_dir_str = params['yaw_dir'].lower()
        if yaw_dir_str == 'clockwise':
            yaw_direction = True
        elif yaw_dir_str == 'counterclockwise':
            yaw_direction = False
        else:
            print("Invalid yaw direction: {}".format(yaw_dir_str))
            return 'Invalid command'
        
        yaw_steps = int(params['yaw_steps'])
        print("Yaw direction: {}, steps: {}".format('clockwise' if yaw_direction else 'counterclockwise', yaw_steps))
        
        # Parse pitch direction and steps
        pitch_dir_str = params['pitch_dir'].lower()
        if pitch_dir_str == 'clockwise':
            pitch_direction = True
        elif pitch_dir_str == 'counterclockwise':
            pitch_direction = False
        else:
            print("Invalid pitch direction: {}".format(pitch_dir_str))
            return 'Invalid command'
        
        pitch_steps = int(params['pitch_steps'])
        print("Pitch direction: {}, steps: {}".format('clockwise' if pitch_direction else 'counterclockwise', pitch_steps))
        
        # Move yaw motor
        print("Moving yaw motor...")
        motor_yaw.set_direction(clockwise=yaw_direction)
        motor_yaw.move_steps(yaw_steps, delay=delay_time)
        
        # Move pitch motor
        print("Moving pitch motor...")
        motor_pitch.set_direction(clockwise=pitch_direction)
        motor_pitch.move_steps(pitch_steps, delay=delay_time)
        
        response = ('Yaw motor moved {} {} steps and Pitch motor moved {} {} steps'.format(
                    'clockwise' if yaw_direction else 'counterclockwise',
                    yaw_steps,
                    'clockwise' if pitch_direction else 'counterclockwise',
                    pitch_steps))
        print("Response:", response)
        return response
    
    except ValueError as ve:
        print("ValueError: {}".format(ve))
        return 'Invalid command: steps must be integers'
    except Exception as e:
        print("Exception: {}".format(e))
        return 'Invalid command: {}'.format(e)

# Setup a simple web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)
print('Listening on', addr)

while True:
    conn, addr = server.accept()
    print('\n--- Connection Established ---')
    print('Connection from', addr)
    request = conn.recv(1024)
    print("Received request:", request)
    response = handle_request(request)
    
    # Prepare the HTTP response
    http_response = 'HTTP/1.1 200 OK\r\n'
    http_response += 'Content-Type: text/plain\r\n'
    http_response += 'Connection: close\r\n\r\n'
    http_response += response
    
    # Send the response
    conn.sendall(http_response)
    conn.close()
    print("--- Connection Closed ---\n")
