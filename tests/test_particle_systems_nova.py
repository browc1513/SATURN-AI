import sys
import os
import numpy as np  # Import numpy for array manipulation

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from physics_subsystems.particle_systems import (
    center_of_mass, total_momentum, collision_momentum, impulse_momentum
)

# Sample input for testing
masses = [1, 2, 3]  # kg
positions = np.array([[1, 1], [2, 2], [3, 3]])  # Convert to numpy arrays for consistency
velocities = np.array([[1, 0], [0, 1], [-1, -1]])  # m/s (now as numpy arrays)
m1, m2 = 2, 3
v1, v2 = np.array([1, 0]), np.array([0, 1])  # Convert velocity vectors to numpy arrays

# Call each function and print the results
print("Center of Mass:", center_of_mass(masses, positions))
print("Total Momentum:", total_momentum(masses, velocities))
print("Collision Momentum (Elastic):", collision_momentum(m1, v1, m2, v2, is_elastic=True))
print("Impulse-Momentum:", impulse_momentum(m1, 0, 10))
