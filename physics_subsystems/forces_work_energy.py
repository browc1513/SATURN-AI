import numpy as np
from math_engine import *  # Preemptive import for future expansion
from core.nova_instance import nova

nova.react_to_task("math")  # Still fits under Science Mode

# Newton's Second Law: F = m * a
def force(mass, acceleration):
    nova.speak("Applying Newton’s Second Law. May the force be with you.")
    return mass * acceleration

# Work: W = F * d * cos(theta)
def work(force, displacement, angle=0):
    nova.speak("Calculating work done—how much effort are we talking?")
    return force * displacement * np.cos(np.radians(angle))

# Power: P = W / t
def power(work, time):
    if time == 0:
        nova.speak("Time is zero. Infinite power? That’s... not how this works.")
        return np.inf
    nova.speak("Determining power output—cue dramatic music.")
    return work / time

# Kinetic Energy: KE = 1/2 * m * v^2
def kinetic_energy(mass, velocity):
    nova.speak("Evaluating kinetic energy. Things are in motion!")
    return 0.5 * mass * velocity**2

# Potential Energy: PE = m * g * h
def potential_energy(mass, height, g=9.81):
    nova.speak("Measuring potential energy. It's all about the drop.")
    return mass * g * height

# Momentum: p = m * v
def momentum(mass, velocity):
    nova.speak("Momentum time. Let’s get moving.")
    return mass * velocity

# Impulse: J = F * t
def impulse(force, time):
    nova.speak("Impulse incoming—forces over time pack a punch.")
    return force * time
