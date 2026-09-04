from sympy import Matrix


def rref(matrix):
    """
    Convert an augmented matrix to Reduced Row Echelon Form.

    Parameters:
        matrix: A list of lists representing the augmented matrix.

    Returns:
        The matrix in RREF and its pivot columns.
    """

    matrix = Matrix(matrix)

    rref_matrix, pivot_columns = matrix.rref()

    return rref_matrix, pivot_columns