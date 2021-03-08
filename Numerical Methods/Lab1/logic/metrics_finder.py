import numpy as np
import math
import logic.inverse_matrix_finder_jordan as inverse_matrix_finder


def find_cond(A):
    norm_a = find_norm(A)
    inverse_a = inverse_matrix_finder.find_inverse(A)
    norm_inverse_a = find_norm(inverse_a)
    return norm_a * norm_inverse_a


def find_norm(A):
    s = 0

    for row in A:
        if len(A.shape) == 2:
            for a in row:
                s += a ** 2
        else:
            s += row ** 2
    return math.sqrt(s)
