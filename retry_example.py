import time
import random

def retry(operation, attempts=3, delay=1):
    for attempt in range(attempts):
        try:
            return operation()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
            delay = delay * 2  # Exponential backoff
    raise Exception("All attempts failed")

# Example operation
def sample_operation():
    print("Trying to connect...")
    if random.random() < 0.7:  # Simulating a 70% failure rate
        raise Exception("Connection failed")
    return "Connected"

# Usage
try:
    result = retry(sample_operation)
    print(result)
except Exception as e:
    print(e)