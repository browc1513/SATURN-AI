import sys
import os
import numpy as np  # Import numpy for array manipulation

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from physics_subsystems.two_d_motion import (
    vector_displacement, vector_velocity, projectile_range, projectile_max_height, projectile_time_of_flight
)

# Sample input for testing
r0 = np.array([0, 0])  # initial position as numpy array
v0 = np.array([10, 15])  # initial velocity as numpy array
a = np.array([0, -9.81])  # acceleration as numpy array
t = 5  # seconds
angle = 45  # degrees

# Call each function and print the results
print("Vector Displacement:", vector_displacement(r0, v0, a, t))
print("Vector Velocity:", vector_velocity(v0, a, t))
print("Projectile Range:", projectile_range(v0[0], angle))
print("Projectile Max Height:", projectile_max_height(v0[1], angle))
print("Projectile Time of Flight:", projectile_time_of_flight(v0[1], angle))
