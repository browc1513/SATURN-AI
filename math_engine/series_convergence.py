import sympy as sp
import numpy as np

def nth_term_test(a_n, n):
    """ Step 2: Apply the nth-Term Test for Divergence """
    limit = sp.limit(a_n, n, sp.oo)
    if limit != 0:
        return "Diverges (nth-Term Test)"
    return "Inconclusive (apply further tests)"

def integral_test(a_n, n):
    """ Step 3: Apply the Integral Test if function is positive, continuous, and decreasing """
    integral = sp.integrate(a_n, (n, 1, sp.oo))
    if integral.is_finite:
        return "Converges (Integral Test)"
    return "Diverges (Integral Test)"

def ratio_test(a_n, n):
    """ Step 3: Apply the Ratio Test """
    ratio = sp.limit(abs(a_n.subs(n, n + 1) / a_n), n, sp.oo)
    if ratio < 1:
        return "Converges (Ratio Test)"
    elif ratio > 1:
        return "Diverges (Ratio Test)"
    return "Inconclusive"

def comparison_test(a_n, b_n, n):
    """ Step 3: Apply the Comparison Test with a known b_n """
    limit = sp.limit(a_n / b_n, n, sp.oo)
    if limit > 0 and sp.summation(b_n, (n, 1, sp.oo)).is_finite:
        return "Converges (Comparison Test)"
    elif limit > 0 and not sp.summation(b_n, (n, 1, sp.oo)).is_finite:
        return "Diverges (Comparison Test)"
    return "Inconclusive"

def absolute_or_conditional_convergence(a_n, n):
    """ Step 4: Determine Absolute or Conditional Convergence """
    abs_series = sp.summation(abs(a_n), (n, 1, sp.oo))
    orig_series = sp.summation(a_n, (n, 1, sp.oo))
    
    if abs_series.is_finite:
        return "Absolutely Convergent"
    elif orig_series.is_finite:
        return "Conditionally Convergent"
    return "Divergent"

def evaluate_series(a_n):
    """ Step 1-4: Full Evaluation Pipeline """
    n = sp.symbols('n', integer=True, positive=True)

    # Step 1: Identify the Type of Series
    print("Step 1: Identifying Series Type...")
    if a_n.match(sp.Geometric(n)):
        print("Geometric Series Identified.")
    elif a_n.match(1 / n**sp.Symbol('p')):
        print("p-Series Identified.")
    elif (-1)**n in a_n.free_symbols:
        print("Alternating Series Identified.")
    else:
        print("General Series Identified.")

    # Step 2: nth-Term Test for Divergence
    print("\nStep 2: Applying nth-Term Test...")
    result = nth_term_test(a_n, n)
    print("Result:", result)
    if "Diverges" in result:
        return

    # Step 3: Apply a Convergence Test
    print("\nStep 3: Applying Convergence Tests...")
    tests = [integral_test, ratio_test]
    for test in tests:
        result = test(a_n, n)
        print("Result:", result)
        if "Converges" in result or "Diverges" in result:
            break

    # Step 4: Absolute or Conditional Convergence
    print("\nStep 4: Checking Absolute or Conditional Convergence...")
    result = absolute_or_conditional_convergence(a_n, n)
    print("Final Conclusion:", result)

# Example Usage
n = sp.symbols('n', integer=True, positive=True)
a_n = (-1)**n / n  # Alternating Harmonic Series
evaluate_series(a_n)
