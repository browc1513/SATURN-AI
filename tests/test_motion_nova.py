import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from physics_subsystems.motion import (
    displacement, final_velocity, velocity_squared
)

# Sample input for testing
v0 = 0  # m/s
a = 9.81  # m/s²
t = 5  # seconds
s = 100  # meters

# Call each function and print the results
print("Displacement:", displacement(v0, a, t))
print("Final Velocity:", final_velocity(v0, a, t))
print("Velocity Squared:", velocity_squared(v0, a, s))
