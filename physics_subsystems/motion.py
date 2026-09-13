import numpy as np
from math_engine import *
from core.saturn_instance import get_saturn

saturn = get_saturn("saturn_config.json")

def displacement(v0, a, t):
    """Computes displacement using s = v0*t + (1/2)*a*t^2"""
    saturn.speak("Calculating displacement. Motion in progress—no speed limit violations, please.")
    return v0 * t + 0.5 * a * (t ** 2)

def final_velocity(v0, a, t):
    """Computes final velocity using v = v0 + a*t"""
    saturn.speak("Solving for final velocity. Let’s see where we end up.")
    return v0 + a * t

def velocity_squared(v0, a, s):
    """Computes velocity using v^2 = v0^2 + 2*a*s"""
    saturn.speak("Computing velocity from distance—kinematics style.")
    return np.sqrt(v0 ** 2 + 2 * a * s)
