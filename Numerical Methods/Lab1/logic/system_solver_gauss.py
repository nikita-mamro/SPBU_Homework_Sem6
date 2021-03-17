import numpy as np


def find_solution(A, b, use_pivoting=False):
    '''
    Find x for Ax=b equation using Gaussian method

    Parameters
    ----
    A
        Matrix A from equation
    b
        Vector b from equation
    use_pivoting
        Flag to choose option whether to select max pivot or not
    ----

    Raises
    ----
    ValueError
        If sizes of A and b are incompatible or error occured in selecting pivot
    ----

    Returns
    ----
    x
        Vector x --- solution of system
    ----
    '''
    n = len(A)
    if b.size != n:
        raise ValueError('Incompatible sizes of A and b')

    for i in range(n - 1):
        if use_pivoting:
            pivot_index = abs(A[i:, i]).argmax() + i
            if A[pivot_index, i] == 0:
                raise ValueError('A is singular')

            if pivot_index != i:
                A[[i, pivot_index]] = A[[pivot_index, i]]
                b[[i, pivot_index]] = b[[pivot_index, i]]
        else:
            if A[i, i] == 0:
                raise ValueError('Pivot is zero')

        for j in range(i + 1, n):
            ratio = A[j, i] / A[i, i]
            A[j, i:] -= ratio * A[i, i:]
            b[j] -= ratio * b[i]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return x
