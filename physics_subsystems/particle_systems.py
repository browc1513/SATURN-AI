import numpy as np
from math_engine import *  # For future expansion with calculus operations

# Center of Mass: R = (Σ m_i * r_i) / Σ m_i
def center_of_mass(masses, positions):
    """
    Computes the center of mass of a system of particles.
    :param masses: List of masses [m1, m2, m3, ...]
    :param positions: List of position vectors [[x1, y1], [x2, y2], ...]
    :return: Center of mass vector [x_com, y_com]
    """
    masses = np.array(masses)
    positions = np.array(positions)

    if len(masses) != len(positions):
        raise ValueError("Mass and position lists must be the same length.")

    total_mass = np.sum(masses)
    if total_mass == 0:
        raise ValueError("Total mass cannot be zero.")

    return np.sum(masses[:, np.newaxis] * positions, axis=0) / total_mass

# Linear Momentum: P = Σ m_i * v_i
def total_momentum(masses, velocities):
    """
    Computes the total linear momentum of a system of particles.
    :param masses: List of masses [m1, m2, m3, ...]
    :param velocities: List of velocity vectors [[vx1, vy1], [vx2, vy2], ...]
    :return: Total momentum vector [Px, Py]
    """
    masses = np.array(masses)
    velocities = np.array(velocities)

    if len(masses) != len(velocities):
        raise ValueError("Mass and velocity lists must be the same length.")

    return np.sum(masses[:, np.newaxis] * velocities, axis=0)

# Collision (Elastic & Inelastic) Momentum Conservation
def collision_momentum(m1, v1, m2, v2, is_elastic=True):
    """
    Computes final velocities of two particles after a collision.
    :param m1, m2: Masses of the two objects
    :param v1, v2: Initial velocities of the objects
    :param is_elastic: True for elastic, False for inelastic
    :return: (v1_final, v2_final) for elastic, (v_final) for inelastic
    """
    if is_elastic:
        v1_final = ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2
        v2_final = ((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2
        return v1_final, v2_final
    else:
        v_final = (m1 * v1 + m2 * v2) / (m1 + m2)
        return v_final

# Impulse-Momentum Theorem: J = Δp = m * Δv
def impulse_momentum(mass, v_initial, v_final):
    """
    Computes impulse given initial and final velocity.
    :param mass: Mass of the object
    :param v_initial: Initial velocity
    :param v_final: Final velocity
    :return: Impulse (change in momentum)
    """
    return mass * (v_final - v_initial)
