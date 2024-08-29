import requests as r
import time

url = "http://192.168.4.80/control?yaw_dir=clockwise&yaw_steps=200&pitch_dir=counterclockwise&pitch_steps=0"

# List to store the duration of each request
durations = []

# Perform 20 requests
for i in range(20):
    # Record the start time
    start_time = time.time()
    
    # Send the HTTP GET request
    response = r.get(url)
    
    # Record the end time
    end_time = time.time()
    
    # Calculate the duration
    duration = end_time - start_time
    durations.append(duration)
    
    # Print the response status and time taken for each request
    print(f"Request {i+1} - Status Code: {response.status_code}, Time: {duration:.4f} seconds")

# Calculate statistics
average_time = sum(durations) / len(durations)
min_time = min(durations)
max_time = max(durations)

# Print summary statistics
print("\nSummary Statistics for 20 Requests:")
print(f"Average Time: {average_time:.4f} seconds")
print(f"Minimum Time: {min_time:.4f} seconds")
print(f"Maximum Time: {max_time:.4f} seconds")
