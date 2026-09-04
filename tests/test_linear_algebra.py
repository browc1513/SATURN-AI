from math_engine.linear_algebra import rref

matrix = [
    [1, 1, 1, 8],
    [0, 2, 1, 5],
    [0, 0, 3, 9]
]

result, pivots = rref(matrix)

print(result)