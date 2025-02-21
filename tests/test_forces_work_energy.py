import pytest
import numpy as np
from physics_subsystems.forces_work_energy import (
    force,
    work,
    power,
    kinetic_energy,
    potential_energy,
    momentum,
    impulse,
)

def test_force():
    assert force(10, 5) == 50  # F = 10kg * 5m/s²

def test_work():
    assert work(20, 10, 0) == 200  # W = 20N * 10m * cos(0°)

def test_power():
    assert power(200, 4) == 50  # P = 200J / 4s

def test_kinetic_energy():
    assert kinetic_energy(5, 3) == pytest.approx(22.5, rel=1e-5)  # KE = 1/2 * 5kg * (3m/s)^2

def test_potential_energy():
    assert potential_energy(10, 2) == pytest.approx(196.2, rel=1e-5)  # PE = 10kg * 9.81m/s² * 2m

def test_momentum():
    assert momentum(4, 8) == 32  # p = 4kg * 8m/s

def test_impulse():
    assert impulse(10, 3) == 30  # J = 10N * 3s
