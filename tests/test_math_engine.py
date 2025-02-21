import sys
import os
import unittest
import numpy as np

# Ensure Python finds math_engine.py inside the math_engine/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "math_engine")))

from math_engine import *  # Now it should import correctly

class TestMathEngine(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(3, 2), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(0, 5), -5)

    def test_multiply(self):
        self.assertEqual(multiply(3, 3), 9)
        self.assertEqual(multiply(-2, 5), -10)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertRaises(ValueError, divide, 5, 0)  # Ensure it handles divide by zero

    def test_differentiate(self):
        def func(x):  # Define a proper function instead of lambda
            return x**2  # f(x) = x^2 → f'(x) = 2x
        self.assertAlmostEqual(differentiate(func, 3), 6, places=4)

    def test_integrate(self):
        def func(x):  # Ensure integration uses a proper function
            return x  # ∫x dx from 0 to 2 = (1/2)x^2 | 0 to 2 = 2
        self.assertAlmostEqual(integrate(func, 0, 2), 2, places=4)

    def test_matrix_operations(self):
        A = np.array([[2, 1], [1, 2]])
        B = np.array([[1, 0], [0, 1]])

        self.assertTrue(np.array_equal(matrix_multiply(A, B), A))
        self.assertAlmostEqual(matrix_determinant(A), 3)
        self.assertTrue(np.allclose(matrix_inverse(A), np.array([[2/3, -1/3], [-1/3, 2/3]])))

    def test_fourier_transform(self):
        signal = np.array([1, 2, 3, 4])
        freq_data = fourier_transform(signal)
        reconstructed_signal = inverse_fourier_transform(freq_data)

        self.assertTrue(np.allclose(signal, reconstructed_signal.real))  # Ensure reconstruction is accurate
