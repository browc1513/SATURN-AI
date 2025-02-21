import numpy as np
from scipy.optimize import approx_fprime  # Fix for deprecated derivative function
from scipy.integrate import quad
from numpy.linalg import inv, det, eig
from numpy import mean, std
from scipy.stats import norm
from numpy.fft import fft, ifft

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
        raise ValueError("Cannot divide by zero.")
    return a / b

# Calculus Operations
def differentiate(func, x, dx=1e-6):
    """Computes the numerical derivative of a function at point x."""
    grad = approx_fprime(np.array([x]), func, dx)
    return grad[0]

def integrate(func, a, b):
    """Computes the definite integral of a function from a to b."""
    result, _ = quad(func, a, b)
    return result

# Matrix & Linear Algebra Operations
def matrix_multiply(A, B):
    """Returns the product of two matrices A and B."""
    return np.dot(A, B)

def matrix_inverse(A):
    """Returns the inverse of matrix A, if invertible."""
    if det(A) == 0:
        raise ValueError("Matrix is singular and cannot be inverted.")
    return inv(A)

def matrix_determinant(A):
    """Returns the determinant of matrix A."""
    return det(A)

def matrix_eigenvalues(A):
    """Returns the eigenvalues of matrix A."""
    return eig(A)[0]

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
    return fft(signal)

def inverse_fourier_transform(freq_data):
    """Computes the inverse Fourier Transform to reconstruct the original signal."""
    return ifft(freq_data)
