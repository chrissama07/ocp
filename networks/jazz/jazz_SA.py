import random
import math
import time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
import pathes
from networks.jazz import data_jazz

A = data_jazz.A

N = data_jazz.N  # number of nodes

E = data_jazz.E  # number of edges

Cn = data_jazz.Cn  # cost of each vaccine

gamma = data_jazz.gamma  # curing rate

Rou = data_jazz.Rou

first_delta = np.loadtxt(pathes.jazz_initial)

""":parameter for SA"""
T_SA = 100
T_max = 100000
T_min = 1
L = 20  # iteration in each temperature
# area
d_max = 0.01  # upper bound
d_min = -0.01  # lower bound
m = 10000  # length of unfeasible solution list
a = 0.9  # Coefficient of variation of T
unfeasible_list = []

interval = 5
delta_list_SA = np.empty([T_SA // interval + 1])


class X:
    delta = np.empty([N])
    fit = 0
    feas = 0

    def fitness_value(self):
        """
        calculate fitness_value
        :param self:   list of vaccination rate
        :return:    fitness value
        """

        fitness = np.multiply(self.delta, Cn).sum()
        # fitness += self.delta[i] * Cn[i]
        return fitness

    def feasible_value(self):
        """
        calculate feasible value
        :return: feasible value
        """
        for i in range(E):
            A[i, 2] = (1.0 - self.delta[int(A[i, 0])] * Rou[int(A[i, 0])]) * (1.0 - self.delta[int(A[i, 1])] * Rou[int(A[i, 0])]) * A[i, 2]

        a = sparse.lil_matrix((N, N))
        for i in range(E):
            a[int(A[i, 0]), int(A[i, 1])] = A[i, 2]
        a = a.tocsr()
        eval_large, eve_large = eigsh(a, 1, which='LM')
        return eval_large

    def get_fit(self):
        self.fit = np.multiply(self.delta, Cn).sum()

    def get_feas(self):
        self.feas = self.feasible_value()

    def get_delta(self, delta):
        self.delta = list(delta)

    def put_delta(self):
        return self.delta

    def put_fit(self):
        return self.fit

    def put_feas(self):
        return self.feas


def calculate_p(fit_new, fit, T):
    """
    calculate p for SA algorithm
    :param fit_new: fitness value of x_new
    :param fit: fitness value of x
    :param T: current temperature
    :return: p
    """
    p = math.exp(- ((fit_new - fit) / T))
    return p


def SA(xx_best):
    """
    SA algorithm
    :param xx_best: best x from DE
    :return: best x after DESA
    """
    # initialize
    t = 0
    T = T_max
    x = xx_best
    xx_best_sa = xx_best

    # SA
    while T > T_min:
        it = 0

        # iteration at current temperature
        while it <= L:
            x_new = X()
            # x_new.delta.clear()

            for i in range(N):
                x_new.delta[i] = x.delta[i] + random.uniform(d_min, d_max)

            # x_new.get_delta(compare_max(x_new.put_delta()))
            # x_new.get_delta(compare_min(x_new.put_delta()))
            x_new.get_fit()
            x_new.get_feas()

            # compare
            if x_new.put_fit() < x.put_fit():
                # x = x_new
                x.get_delta(x_new.put_delta())
                x.get_fit()
                x.get_feas()
            else:
                p = calculate_p(x_new.put_fit(), x.put_fit(), T)
                if p > random.uniform(0, 1):
                    # x = x_new
                    x.get_delta(x_new.put_delta())
                    x.get_fit()
                    x.get_feas()
            it += 1

        # decide whether algorithm ends
        if x.put_feas() <= 0:
            unfeasible_list.clear()
            xx_best_sa = x
        else:
            unfeasible_list.append(x)
            if len(unfeasible_list) == m:
                break

        if t % interval == interval - 1:
            delta_list_SA[t // interval + 1] = xx_best_sa.put_fit()

        t += 1
        if t == T_SA:
            break

        T = a * T

    return xx_best_sa


def main():
    x = X()
    x.get_delta(first_delta)
    x.get_fit()
    x.get_feas()
    delta_list_SA[0] = x.put_fit()
    print(x.put_fit())
    x_best = SA(x)
    print(x_best.put_fit())
    np.savetxt(pathes.jazz_SA_output, delta_list_SA)


main()
