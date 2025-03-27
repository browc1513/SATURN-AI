import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from math_engine.series_convergence import evaluate_series
import sympy as sp

n = sp.symbols('n', integer=True, positive=True)

# Use Piecewise to manually define alternating harmonic series
a_n = sp.Piecewise((1/n, n % 2 != 0), (-1)/n, True)  # Alternating Harmonic Series

evaluate_series(a_n)
