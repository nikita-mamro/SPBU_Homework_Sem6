import numpy as np


def find_determinant(A):
    '''
    Given A, find |A|

    Parameters
    ----
    A --- input matrix
    ----

    Raises
    ----
    ValueError
        A is not square or error occured during LU-decomposition
    ----

    Returns
    ----
    Determinant of A
    ----
    '''
    shape = A.shape
    if len(shape) != 2 or shape[0] != shape[1]:
        raise ValueError('A is not square 2d matrix')

    n = len(A)

    L = np.zeros((n, n))
    U = np.eye(n)

    for i in range(n):
        for j in range(i, n):
            s = 0
            for k in range(0, i - 1):
                s += L[j][k] * U[k][i]

            L[j][i] = A[j][i] - s

            s = 0
            for k in range(0, i - 1):
                s += L[i][k] * U[k][j]

            U[i][j] = (A[i][j] - s) / L[i][i]

    return L.diagonal().prod()
