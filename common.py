# common.py
import random

# Function to generate parameters within given ranges
def generate_engine_speed():
    return random.randint(1200, 1800)

def generate_throttle_setting():
    return random.randint(45, 85)

def generate_implement_depth():
    return round(random.uniform(5, 45), 2)

def generate_actual_forward_speed():
    return round(random.uniform(0.8, 4.5), 2)

# Generate latitude and longitude
def generate_latitude(current_lat):
    return current_lat + random.uniform(-0.0001, 0.0001)

def generate_longitude(current_long):
    return current_long + random.uniform(-0.0001, 0.0001)
