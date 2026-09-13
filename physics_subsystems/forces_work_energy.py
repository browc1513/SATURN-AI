import numpy as np
from core.saturn_instance import get_saturn

saturn = get_saturn("saturn_config.json")

saturn.react_to_task("math")  # Still fits under Science Mode

# Newton's Second Law: F = m * a
def force(mass, acceleration):
    saturn.speak("Applying Newton’s Second Law. May the force be with you.")
    return mass * acceleration

# Work: W = F * d * cos(theta)
def work(force, displacement, angle=0):
    saturn.speak("Calculating work done—how much effort are we talking?")
    return force * displacement * np.cos(np.radians(angle))

# Power: P = W / t
def power(work, time):
    if time == 0:
        saturn.speak("Time is zero. Infinite power? That’s... not how this works.")
        return np.inf
    saturn.speak("Determining power output—cue dramatic music.")
    return work / time

# Kinetic Energy: KE = 1/2 * m * v^2
def kinetic_energy(mass, velocity):
    saturn.speak("Evaluating kinetic energy. Things are in motion!")
    return 0.5 * mass * velocity**2

# Potential Energy: PE = m * g * h
def potential_energy(mass, height, g=9.81):
    saturn.speak("Measuring potential energy. It's all about the drop.")
    return mass * g * height

# Momentum: p = m * v
def momentum(mass, velocity):
    saturn.speak("Momentum time. Let’s get moving.")
    return mass * velocity

# Impulse: J = F * t
def impulse(force, time):
    saturn.speak("Impulse incoming—forces over time pack a punch.")
    return force * time
