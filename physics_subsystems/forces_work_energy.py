import numpy as np
from math_engine import *  # Preemptive import for future expansion

# Newton's Second Law: F = m * a
def force(mass, acceleration):
    return mass * acceleration

# Work: W = F * d * cos(theta)
def work(force, displacement, angle=0):
    return force * displacement * np.cos(np.radians(angle))

# Power: P = W / t
def power(work, time):
    return work / time if time != 0 else np.inf

# Kinetic Energy: KE = 1/2 * m * v^2
def kinetic_energy(mass, velocity):
    return 0.5 * mass * velocity**2

# Potential Energy: PE = m * g * h
def potential_energy(mass, height, g=9.81):
    return mass * g * height

# Momentum: p = m * v
def momentum(mass, velocity):
    return mass * velocity

# Impulse: J = F * t
def impulse(force, time):
    return force * time
