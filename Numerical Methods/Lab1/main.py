import numpy as np
import settings.constants as constants
import logic.system_solver_gauss as system_solver
import logic.inverse_matrix_finder_jordan as inverse_matrix_finder
import logic.matrix_determinant_finder_lu_decomposition as matrix_determinant_finder
import logic.metrics_finder as metrics_finder


def solve_system():
    print('\nРешение системы Ax=b для A и b = (200, -600):\n')
    A = np.copy(constants.A)
    x_accurate = system_solver.find_solution(A, constants.b_a, True)
    print(x_accurate)
    print('\nРешение системы Ax=b для A и b = (199, -601):\n')
    A = np.copy(constants.A)
    x_error = system_solver.find_solution(A, constants.b_b, True)
    print(x_error)
    print('\nЧисло обусловленности A:\n')
    A = np.copy(constants.A)
    condition_number = metrics_finder.find_cond(constants.A)
    print(condition_number)
    print('\nФактическая погрешность:\n')
    actual_error = metrics_finder.find_norm(np.subtract(
        x_accurate, x_error)) / metrics_finder.find_norm(x_accurate)
    print(actual_error)
    print('\nОценка погрешности:\n')
    estimated_error = condition_number * \
        (metrics_finder.find_norm(np.subtract(constants.b_a, constants.b_b))
         ) / metrics_finder.find_norm(constants.b_a)
    print(estimated_error)


def find_inverse():
    print('\nОбратная матрица для M\n')
    inverse_matrix = inverse_matrix_finder.find_inverse(constants.M)
    print(inverse_matrix)


def find_determinant():
    print('\nОпределитель M:\n')
    det = matrix_determinant_finder.find_determinant(constants.M)
    print(det)


def print_divider():
    print('-' * 50)


def main():
    print('Лабораторная работа 1')
    print('Вариант 11')
    print_divider()
    print('Матрица A:')
    print(constants.A)
    print_divider()
    print('Матрица M:')
    print(constants.M)
    print_divider()
    solve_system()
    print_divider()
    find_inverse()
    print_divider()
    find_determinant()


if __name__ == '__main__':
    main()
