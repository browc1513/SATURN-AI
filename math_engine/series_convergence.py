import sympy as sp
import numpy as np
from core.nova_instance import nova

nova.react_to_task("math")  # Switch to Science Mode

def nth_term_test(a_n, n):
    nova.speak("Running the nth-Term Test. Let’s see if this series holds up.")
    limit = sp.limit(a_n, n, sp.oo)
    if limit != 0:
        nova.speak("Limit doesn’t go to zero—this series diverges.")
        return "Diverges (nth-Term Test)"
    return "Inconclusive (apply further tests)"

def integral_test(a_n, n):
    nova.speak("Applying the Integral Test. Calculus, engage!")
    integral = sp.integrate(a_n, (n, 1, sp.oo))
    if integral.is_finite:
        return "Converges (Integral Test)"
    return "Diverges (Integral Test)"

def ratio_test(a_n, n):
    nova.speak("Ratio Test incoming. Let’s see if things shrink fast enough.")
    ratio = sp.limit(abs(a_n.subs(n, n + 1) / a_n), n, sp.oo)
    if ratio < 1:
        return "Converges (Ratio Test)"
    elif ratio > 1:
        return "Diverges (Ratio Test)"
    return "Inconclusive"

def comparison_test(a_n, b_n, n):
    nova.speak("Engaging Comparison Test. Comparing this to something we trust...")
    limit = sp.limit(a_n / b_n, n, sp.oo)
    b_series = sp.summation(b_n, (n, 1, sp.oo))
    if limit > 0 and b_series.is_finite:
        return "Converges (Comparison Test)"
    elif limit > 0 and not b_series.is_finite:
        return "Diverges (Comparison Test)"
    return "Inconclusive"

def absolute_or_conditional_convergence(a_n, n):
    nova.speak("Let’s check if this series is absolutely or conditionally convergent.")
    abs_series = sp.summation(abs(a_n), (n, 1, sp.oo))
    orig_series = sp.summation(a_n, (n, 1, sp.oo))

    if abs_series.is_finite:
        return "Absolutely Convergent"
    elif orig_series.is_finite:
        return "Conditionally Convergent"
    return "Divergent"

def evaluate_series(a_n):
    n = sp.symbols('n', integer=True, positive=True)

    nova.speak("Beginning full series evaluation. Time to classify and conquer.")
    print("Step 1: Identifying Series Type...")

    # Safer series identification
    if a_n.has(sp.Pow) and a_n.as_base_exp()[0] != n:
        print("Geometric Series Identified.")
        nova.speak("Geometric series detected. The classics never disappoint.")
    elif a_n.match(1 / n**sp.Symbol('p')):
        print("p-Series Identified.")
        nova.speak("Ah yes, a p-series. Time to check that exponent.")
    elif (-1)**n in a_n.free_symbols or "(-1)**n" in str(a_n):
        print("Alternating Series Identified.")
        nova.speak("Alternating series? This one’s playing hot and cold.")
    else:
        print("General Series Identified.")
        nova.speak("This one’s a bit trickier—general series mode activated.")

    print("\nStep 2: Applying nth-Term Test...")
    result = nth_term_test(a_n, n)
    print("Result:", result)
    if "Diverges" in result:
        nova.speak("Series diverges—no need to go further.")
        return

    print("\nStep 3: Applying Convergence Tests...")
    tests = [integral_test, ratio_test]
    for test in tests:
        result = test(a_n, n)
        print("Result:", result)
        if "Converges" in result or "Diverges" in result:
            break

    print("\nStep 4: Checking Absolute or Conditional Convergence...")
    result = absolute_or_conditional_convergence(a_n, n)
    print("Final Conclusion:", result)
    nova.speak(f"Final result: {result}. That’s a wrap on this series.")
