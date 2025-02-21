import pytest
import math
from physics_subsystems.two_d_motion import (
    vector_displacement,
    vector_velocity,
    projectile_range,
    projectile_max_height,
    projectile_time_of_flight,
)

def test_vector_displacement():
    result = vector_displacement(3, 4, 0, 0)  # Adjusted for correct function signature
    assert result == pytest.approx(3 + 4 * 0 + 0.5 * 0 * (0 ** 2), rel=1e-5)

def test_vector_velocity():
    result = vector_velocity(10, 2, 5)  # v0 = 10, a = 2, t = 5
    assert result == pytest.approx(20, rel=1e-5)

def test_projectile_range():
    result = projectile_range(20, 45)  # 20 m/s at 45°
    expected = (20**2 * math.sin(math.radians(90))) / 9.81
    assert result == pytest.approx(expected, rel=1e-5)

def test_projectile_max_height():
    result = projectile_max_height(20, 45)
    expected = (20**2 * math.sin(math.radians(45))**2) / (2 * 9.81)
    assert result == pytest.approx(expected, rel=1e-5)

def test_projectile_time_of_flight():
    result = projectile_time_of_flight(20, 45)
    expected = (2 * 20 * math.sin(math.radians(45))) / 9.81
    assert result == pytest.approx(expected, rel=1e-5)
