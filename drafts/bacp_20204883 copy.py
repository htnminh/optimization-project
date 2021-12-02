from ortools.sat.python import cp_model
import numpy as np
import random as rd


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    #print intermediate solution
    def __init__(self,variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print(f'{v}={self.Value(v)}', end = ' ')
        print()
    def solution_count(self):
        return self.__solution_count


def decrease(x): return x - 1


def file_inp(name=r'BACP\bacp-n9-m4.inp'):
    with open(name, 'r') as f:
        n, m = map(int, f.readline().split())
        gamma, lamda = map(int, f.readline().split())
        alpha, beta = map(int, f.readline().split())
        c = list(map(int, f.readline().split()))

        k = int(f.readline())
        prerequisites = []
        for _ in range(k):
            prerequisites.append(list(map(decrease, map(int, f.readline().split()))))

    return n, m, gamma, lamda, alpha, beta, c, k, prerequisites


n, m, gamma, lamda, alpha, beta, c, k, prerequisites = file_inp()
print(n, m, gamma, lamda, alpha, beta, c, k, prerequisites, sep='\n')


model = cp_model.CpModel()

x = [model.NewIntVar(0,m-1,f'x[{i}]') for i in range(n)]


# prerequisites
for i, j in prerequisites:
    model.Add(x[i] < x[j])


# z
z = [[model.NewIntVar(0,1,f'z[{i},{j}]') for j in range(m)] for i in range(n)] 
for i in range(n):
    for j in range(m):
        b = model.NewBoolVar('b')
        model.Add(x[i] == j).OnlyEnforceIf(b)
        model.Add(x[i] != j).OnlyEnforceIf(b.Not())
        model.Add(z[i][j] == 1).OnlyEnforceIf(b)

        b = model.NewBoolVar('b')
        model.Add(x[i] != j).OnlyEnforceIf(b)
        model.Add(x[i] == j).OnlyEnforceIf(b.Not())
        model.Add(z[i][j] == 0).OnlyEnforceIf(b)


for j in range(m):
    # sum_i = sum([z[i][j] for i in range(n)])
    model.Add(alpha <= sum([z[i][j] for i in range(n)]))
    model.Add(sum([z[i][j] for i in range(n)]) <= beta)

    # sum_i_c = sum([z[i][j]*c[i] for i in range(n)])
    model.Add(gamma <= sum([z[i][j]*c[i] for i in range(n)]))
    model.Add(sum([z[i][j]*c[i] for i in range(n)]) <= lamda)

for i in range(n):
    # sum_j = sum([z[i][j] for j in range(m)])
    model.Add(sum([z[i][j] for j in range(m)]) == 1)

solver = cp_model.CpSolver()
solution_printer = VarArraySolutionPrinter(x)
solver.SearchForAllSolutions(model, solution_printer)
