import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import specific functions from the actual math_engine.py file
from math_engine.math_engine import (
    add, subtract, multiply, divide,
    differentiate, integrate,
    matrix_multiply, matrix_inverse, matrix_determinant, matrix_eigenvalues,
    compute_mean, compute_std, normal_distribution,
    fourier_transform, inverse_fourier_transform
)

# Run key functions to trigger N.O.V.A.
print("Add:", add(5, 3))
print("Divide (good):", divide(10, 2))

try:
    print("Divide (bad):", divide(10, 0))
except Exception as e:
    print("Caught error:", e)

print("Derivative:", differentiate(lambda x: x**2, 3))
print("Integral:", integrate(lambda x: x, 0, 5))

A = [[1, 2], [3, 4]]
print("Eigenvalues:", matrix_eigenvalues(A))

signal = [1, 2, 3, 4]
print("Fourier:", fourier_transform(signal))
