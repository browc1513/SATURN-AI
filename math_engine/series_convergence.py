import sympy as sp
import numpy as np
from core.nova_instance import nova

nova.react_to_task("math")  # Switch to Science Mode

def nth_term_test(a_n, n):
    """ Step 2: Apply the nth-Term Test for Divergence """
    nova.speak("Running the nth-Term Test. Let’s see if this series holds up.")
    limit = sp.limit(a_n, n, sp.oo)
    if limit != 0:
        nova.speak("Limit doesn’t go to zero—this series diverges.")
        return "Diverges (nth-Term Test)"
    return "Inconclusive (apply further tests)"

def integral_test(a_n, n):
    """ Step 3: Apply the Integral Test if function is positive, continuous, and decreasing """
    nova.speak("Applying the Integral Test. Calculus, engage!")
    integral = sp.integrate(a_n, (n, 1, sp.oo))
    if integral.is_finite:
        return "Converges (Integral Test)"
    return "Diverges (Integral Test)"

def ratio_test(a_n, n):
    """ Step 3: Apply the Ratio Test """
    nova.speak("Ratio Test incoming. Let’s see if things shrink fast enough.")
    ratio = sp.limit(abs(a_n.subs(n, n + 1) / a_n), n, sp.oo)
    if ratio < 1:
        return "Converges (Ratio Test)"
    elif ratio > 1:
        return "Diverges (Ratio Test)"
    return "Inconclusive"

def comparison_test(a_n, b_n, n):
    """ Step 3: Apply the Comparison Test with a known b_n """
    nova.speak("Engaging Comparison Test. Comparing this to something we trust...")
    limit = sp.limit(a_n / b_n, n, sp.oo)
    b_series = sp.summation(b_n, (n, 1, sp.oo))
    if limit > 0 and b_series.is_finite:
        return "Converges (Comparison Test)"
    elif limit > 0 and not b_series.is_finite:
        return "Diverges (Comparison Test)"
    return "Inconclusive"

def absolute_or_conditional_convergence(a_n, n):
    """ Step 4: Determine Absolute or Conditional Convergence """
    nova.speak("Let’s check if this series is absolutely or conditionally convergent.")
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

    nova.speak("Beginning full series evaluation. Time to classify and conquer.")

    # Step 1: Identify the Type of Series
    print("Step 1: Identifying Series Type...")
    if a_n.match(sp.Geometric(n)):
        print("Geometric Series Identified.")
        nova.speak("Geometric series detected. The classics never disappoint.")
    elif a_n.match(1 / n**sp.Symbol('p')):
        print("p-Series Identified.")
        nova.speak("Ah yes, a p-series. Time to check that exponent.")
    elif (-1)**n in a_n.free_symbols:
        print("Alternating Series Identified.")
        nova.speak("Alternating series? This one’s playing hot and cold.")
    else:
        print("General Series Identified.")
        nova.speak("This one’s a bit trickier—general series mode activated.")

    # Step 2: nth-Term Test for Divergence
    print("\nStep 2: Applying nth-Term Test...")
    result = nth_term_test(a_n, n)
    print("Result:", result)
    if "Diverges" in result:
        nova.speak("Series diverges—no need to go further.")
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
    nova.speak(f"Final result: {result}. That’s a wrap on this series.")

# Example Usage
n = sp.symbols('n', integer=True, positive=True)
a_n = (-1)**n / n  # Alternating Harmonic Series
evaluate_series(a_n)
