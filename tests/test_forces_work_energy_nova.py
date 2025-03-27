import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from physics_subsystems.forces_work_energy import (
    force, work, power, kinetic_energy, potential_energy, momentum, impulse
)

# Create sample input values for testing
mass = 10  # kg
acceleration = 9.81  # m/s²
displacement = 5  # meters
velocity = 20  # m/s
height = 10  # meters
force_value = force(mass, acceleration)

# Call each function and print the results
print("Force:", force_value)
print("Work:", work(force_value, displacement))
print("Power:", power(work(force_value, displacement), 2))
print("Kinetic Energy:", kinetic_energy(mass, velocity))
print("Potential Energy:", potential_energy(mass, height))
print("Momentum:", momentum(mass, velocity))
print("Impulse:", impulse(force_value, 2))
