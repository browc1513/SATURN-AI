import pytest
import numpy as np
from physics_subsystems.particle_systems import (
    center_of_mass,
    total_momentum,
    collision_momentum,
    impulse_momentum,
)

def test_center_of_mass():
    masses = [2, 3, 5]
    positions = [[1, 2], [3, 4], [5, 6]]
    expected = [(2*1 + 3*3 + 5*5) / 10, (2*2 + 3*4 + 5*6) / 10]  # (3.7, 4.7)
    assert np.allclose(center_of_mass(masses, positions), expected, rtol=1e-5)

def test_total_momentum():
    masses = [2, 3]
    velocities = [[1, 2], [3, 4]]
    expected = [2*1 + 3*3, 2*2 + 3*4]  # (11, 16)
    assert np.allclose(total_momentum(masses, velocities), expected, rtol=1e-5)

def test_collision_momentum_elastic():
    v1_final, v2_final = collision_momentum(2, 3, 3, -2, is_elastic=True)
    expected_v1_final = ((2 - 3) / (2 + 3)) * 3 + ((2 * 3) / (2 + 3)) * -2
    expected_v2_final = ((2 * 2) / (2 + 3)) * 3 + ((3 - 2) / (2 + 3)) * -2
    assert pytest.approx(v1_final, rel=1e-5) == expected_v1_final
    assert pytest.approx(v2_final, rel=1e-5) == expected_v2_final

def test_collision_momentum_inelastic():
    v_final = collision_momentum(2, 3, 3, -2, is_elastic=False)
    expected_v_final = (2*3 + 3*(-2)) / (2 + 3)
    assert pytest.approx(v_final, rel=1e-5) == expected_v_final

def test_impulse_momentum():
    assert impulse_momentum(4, 2, 6) == 4 * (6 - 2)  # 4 * 4 = 16
