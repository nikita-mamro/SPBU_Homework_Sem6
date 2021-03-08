import numpy as np


def find_inverse(A):
    '''
    Given A, find A^-1

    Parameters
    ----
    A --- input matrix
    ----

    Raises
    ----
    ValueError
        A is not square or error occured during Gauss Jordan elimination
    ----

    Returns
    ----
    B
        Inverse of A
    ----
    '''
    shape = A.shape
    if len(shape) != 2 or shape[0] != shape[1]:
        raise ValueError('A is not square 2d matrix')

    n = len(A)

    B = np.eye(n)

    # Elimination
    for i in range(n):
        if A[i][i] == 0:
            raise ValueError('Pivot is zero applying Gauss Jordan elimination')

        for j in range(n):
            if i != j:
                ratio = A[j, i] / A[i, i]

                for k in range(n):
                    A[j][k] = A[j][k] - ratio * A[i][k]
                    B[j][k] = B[j][k] - ratio * B[i][k]

    # Normalization
    for i in range(n):
        B[i] /= A[i][i]

    return B
