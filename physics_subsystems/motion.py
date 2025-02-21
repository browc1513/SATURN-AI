import numpy as np
from math_engine import *

def displacement(v0, a, t):
    """Computes displacement using s = v0*t + (1/2)*a*t^2"""
    return v0 * t + 0.5 * a * (t ** 2)

def final_velocity(v0, a, t):
    """Computes final velocity using v = v0 + a*t"""
    return v0 + a * t

def velocity_squared(v0, a, s):
    """Computes velocity using v^2 = v0^2 + 2*a*s"""
    return np.sqrt(v0 ** 2 + 2 * a * s)
