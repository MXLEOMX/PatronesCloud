import time
import random

class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def call(self, operation):
        if self.state == "OPEN":
            if (time.time() - self.last_failure_time) > self.recovery_timeout:
                self.state = "HALF-OPEN"
            else:
                raise Exception("Circuit is open")

        try:
            result = operation()
            self.reset()
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise e

    def reset(self):
        self.failure_count = 0
        self.state = "CLOSED"

# Example operation
def unreliable_operation():
    print("Trying to connect...")
    if random.random() < 0.7:  # Simulating a 70% failure rate
        raise Exception("Connection failed")
    return "Connected"

# Usage
circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=5)

try:
    result = circuit_breaker.call(unreliable_operation)
    print(result)
except Exception as e:
    print(e)