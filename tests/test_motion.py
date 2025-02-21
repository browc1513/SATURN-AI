import sys
import os
import unittest
import numpy as np

# Ensure Python finds motion.py inside the physics_subsystems/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "physics_subsystems")))

from motion import *

class TestMotion(unittest.TestCase):

    def test_displacement(self):
        """Test displacement formula s = v0*t + (1/2)*a*t^2"""
        self.assertAlmostEqual(displacement(2, 3, 4), 32)  # s = 2(4) + (1/2)(3)(16) = 32
        self.assertAlmostEqual(displacement(0, 9.8, 2), 19.6)  # Free fall

    def test_final_velocity(self):
        """Test final velocity formula v = v0 + at"""
        self.assertAlmostEqual(final_velocity(3, 4, 5), 23)  # v = 3 + (4)(5) = 23
        self.assertAlmostEqual(final_velocity(0, 9.8, 2), 19.6)  # Free fall

    def test_velocity_squared(self):
        """Test velocity squared formula v^2 = v0^2 + 2as"""
        self.assertAlmostEqual(velocity_squared(0, 9.8, 10), np.sqrt(196))  # v^2 = 2(9.8)(10) = 196, v = sqrt(196)
        self.assertAlmostEqual(velocity_squared(3, 4, 5), np.sqrt(3**2 + 2*4*5))  # v^2 = 9 + 40 = 49, v = sqrt(49)

if __name__ == "__main__":
    unittest.main()
