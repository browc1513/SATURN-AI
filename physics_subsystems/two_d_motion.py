import numpy as np
from math_engine import *

def vector_displacement(r0, v0, a, t):
    """Computes displacement vector using r = r0 + v0*t + (1/2)*a*t^2"""
    return r0 + v0 * t + 0.5 * a * (t ** 2)

def vector_velocity(v0, a, t):
    """Computes velocity vector using v = v0 + a*t"""
    return v0 + a * t

def projectile_range(v0, angle, g=9.81):
    """Computes the range of a projectile launched at an angle"""
    vx = v0 * np.cos(np.radians(angle))
    vy = v0 * np.sin(np.radians(angle))
    time_of_flight = (2 * vy) / g
    return vx * time_of_flight

def projectile_max_height(v0, angle, g=9.81):
    """Computes the max height of a projectile launched at an angle"""
    vy = v0 * np.sin(np.radians(angle))
    return (vy ** 2) / (2 * g)

def projectile_time_of_flight(v0, angle, g=9.81):
    """Computes the time of flight of a projectile"""
    vy = v0 * np.sin(np.radians(angle))
    return (2 * vy) / g
