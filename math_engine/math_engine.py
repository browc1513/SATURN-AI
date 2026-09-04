import numpy as np
from scipy.optimize import approx_fprime
from scipy.integrate import quad
from numpy.linalg import inv, det, eig
from numpy import mean, std
from scipy.stats import norm
from numpy.fft import fft, ifft

from math_engine.linear_algebra import rref

from core.nova_instance import get_nova

nova = get_nova("nova_config.json")

nova.react_to_task("math")  # Activates Science Mode

# Basic Arithmetic Operations
def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Returns the difference of two numbers."""
    return a - b

def multiply(a, b):
    """Returns the product of two numbers."""
    return a * b

def divide(a, b):
    """Returns the quotient of two numbers. Handles division by zero."""
    if b == 0:
        nova.speak("Uh-oh, dividing by zero? Even I can't help with that.")
        raise ValueError("Cannot divide by zero.")
    return a / b

# Calculus Operations
def differentiate(func, x, dx=1e-6):
    """Computes the numerical derivative of a function at point x."""
    nova.speak("Crunching the slope—let’s find that derivative.")
    grad = approx_fprime(np.array([x]), func, dx)
    return grad[0]

def integrate(func, a, b):
    """Computes the definite integral of a function from a to b."""
    nova.speak(f"Integrating from {a} to {b}. This might get... irrational.")
    result, _ = quad(func, a, b)
    return result

# Matrix & Linear Algebra Operations
def matrix_multiply(A, B):
    """Returns the product of two matrices A and B."""
    return np.dot(A, B)

def matrix_inverse(A):
    """Returns the inverse of matrix A, if invertible."""
    if det(A) == 0:
        nova.speak("That matrix is singular. It cannot be inverted—like some people.")
        raise ValueError("Matrix is singular and cannot be inverted.")
    return inv(A)

def matrix_determinant(A):
    """Returns the determinant of matrix A."""
    return det(A)

def matrix_eigenvalues(A):
    """Returns the eigenvalues of matrix A."""
    nova.speak("Finding eigenvalues... or as I like to call them, the matrix’s inner thoughts.")
    return eig(A)[0]

def matrix_rref(A):
    """Returns the Reduced Row Echelon Form of matrix A."""

    rref_matrix, pivot_columns = rref(A)

    return rref_matrix, pivot_columns

# Statistical & Probability Functions
def compute_mean(data):
    """Returns the mean (average) of a dataset."""
    return mean(data)

def compute_std(data):
    """Returns the standard deviation of a dataset."""
    return std(data)

def normal_distribution(x, mu=0, sigma=1):
    """Returns the probability density of x in a normal distribution."""
    return norm.pdf(x, mu, sigma)

# Fourier Transform for Signal Processing
def fourier_transform(signal):
    """Computes the Fourier Transform of a given signal."""
    nova.speak("Shifting to the frequency domain. Hang on tight.")
    return fft(signal)

def inverse_fourier_transform(freq_data):
    """Computes the inverse Fourier Transform to reconstruct the original signal."""
    nova.speak("Reconstructing the original signal. Fourier would be proud.")
    return ifft(freq_data)
