from core import *
import numpy as np

def matmet(System):

    """ Solve a system of linear equations by the matrix method """

    Matrix_A = System['A']
    Matrix_B = System['B']
    Vars = System['X']

    if len(Matrix_A) != len(Matrix_B):
        raise SyntaxError(
            "The system of linear equations should have the form of a square matrix")

    Matrix_A_inv = np.linalg.inv(Matrix_A)
    Values = list(np.array(Matrix_A_inv.dot(Matrix_B)).reshape(-1,))

    return {Vars[i]: Values[i] for i in range(len(Vars))}

if __name__ == '__main__':

    list_of_equations = []

    print("Система линейных уравнений:")

    while True:

        lineq = str(input())

        if lineq == '':
            break

        else:
            list_of_equations.append(Equation(lineq))

    System = Equation.system(list_of_equations)
    Solved_system = matmet(System)

    print("Ответы:")

    for var in Solved_system:
        print(f'{var} = {Solved_system[var]}')
