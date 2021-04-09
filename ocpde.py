import random
import math
import time
# import data_email
import data_email
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

# A = data_email.A
# 
# N = data_email.N  # number of nodes
# 
# E = data_email.E  # number of edges
# 
# Cn = data_email.Cn    # cost of each vaccine
# 
# gamma = data_email.gamma  # curing rate

A = data_email.A

N = data_email.N  # number of nodes

E = data_email.E  # number of edges

Cn = data_email.Cn    # cost of each vaccine

gamma = data_email.gamma  # curing rate

""":parameter: for DE"""
no = 5  # number of nodes generated by each node
CR = 0.7  # rate of crossover
T_DE = 20  # iteration of DE

""":parameter k and F: for current/rand/1"""
k = 0.5
F = 0.8

""":parameter for crossoverSBX"""
sbx_n = 1.1

""":parameter for SA"""                                                     
T_max = 1000
T_min = 10
L = 20  # iteration in each temperature
# area
d_max = 0.00005  # upper bound
d_min = -0.00005  # lower bound
m = 10  # length of unfeasible solution list
a = 0.8  # Coefficient of variation of T
unfeasible_list = []


# class of X
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
        # A_ = np.zeros([N, N])
        # for i in range(N):
        #     for j in range(N):
        #         if A[i][j] != 0:
        #             A_[i][j] = (1.0 - self.delta[i]) * (1.0 - self.delta[j]) * A[i][j]
        # return max(np.linalg.eigvals(A_ - np.diag(gamma)))

        for i in range(E):
            A[i, 2] = (1.0 - self.delta[int(A[i, 0])]) * (1.0 - self.delta[int(A[i, 1])]) * A[i, 2]

        a = sparse.lil_matrix((N, N))
        for i in range(E):
            a[int(A[i, 0]), int(A[i, 1])] = A[i, 2]
        a = a.tocsr()
        eval_large, eve_large = eigsh(a, 1, which='LM')
        return eval_large

        # A_ = A
        # for i in range(N):
        #     for j in range(len(A_[i].indices)):
        #         index = A_[i].indices[j]
        #         A_[i, index] = (1.0 - self.delta[i]) * (1.0 - self.delta[index]) * A[i, index]

        # for i in range(N):
        #     for j in range(N):
        #         if A[i, j] != 0:

        #             A_[i, j] = (1.0 - self.delta[i]) * (1.0 - self.delta[j]) * A[i, j]
        # for i in range(N):
        #     max_index = 0
        #     for j in range(len(A.indices)):
        #         index = A.indices[j]
        #         if index > max_index:
        #             A_[i, index] = (1.0 - self.delta[i]) * (1.0 - self.delta[index]) * A[i, index]
        # A_ = A_.toscr()
        # evals_large, evecs_large = eigsh(A_, 1, which='LM')
        # return evals_large

    def get_fit(self):
        self.fit = np.multiply(self.delta, Cn).sum()
        # for i in range(N):
        #     self.fit += np.multiply(self.delta, Cn)
            # self.fit += self.delta[i] * Cn[i]

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


def current_to_rand(xx_list, r1, r2, r3, i):
    """
    current/rand/1
    :param xx_list:
    :param r1: vec{x_{r1}}
    :param r2: vec{x_{r2}}
    :param r3: vec{x_{r3}}
    :param i: vec{x_{i}}
    :return: vec{v_{j}}.delta
    """
    v_delta = np.add(xx_list[i].delta, k * np.subtract(xx_list[r1].delta, xx_list[i].delta),
                     F * np.subtract(xx_list[r2].delta, xx_list[r3].delta))

    # for j in range(N):
    #     current_delta = xx_list[i].delta[j] + \
    #                     k * (xx_list[r1].delta[j] - xx_list[i].delta[j]) + \
    #                     F * (xx_list[r2].delta[j] - xx_list[r3].delta[j])
    #     v_delta[j] = current_delta
    #     # v_delta.append(current_delta)
    return v_delta


def compare_max(delta):
    """
    lower bound
    :param delta: delta
    :return: turn into lower bound delta
    """

    em = np.zeros([N])
    delta = np.maximum(delta, em)
    # for i in range(len(delta)):
    #     delta[i] = max(delta[i], 0)
    return delta


def compare_min(delta):
    """
    upper bound
    :param delta: delta
    :return: turn into upper bound delta
    """

    on = np.ones([N])
    delta = np.minimum(delta, on)
    # for i in range(len(delta)):
    #     delta[i] = min(delta[i], 1)
    return delta


def select_better_fit(x1, x2):
    """
    select better x with better fit value
    :param x1: first x
    :param x2: second x
    :return: better x with better fit value
    """
    if x1.fit <= x2.fit:
        return x1
    else:
        return x2


def crossover_SBX(xi, vj):
    """
    crossoverSBX
    :param xi: parent
    :param vj: mutation
    :return: crossover
    """
    beta = 0
    while isinstance(beta, complex):  # beta must not be complex
        sbx_rand = random.random()
        if sbx_rand <= 0.5:
            beta = (2 * sbx_rand) ** (1 / (1 + sbx_n))
        else:
            beta = (1 / (2 - sbx_n * 2)) ** (1 / (1 + sbx_n))
    c1 = X()
    c2 = X()
    c1_delta = np.empty([N])
    c2_delta = np.empty([N])
    # c1_delta = []
    # c2_delta = []
    xi_delta = xi.put_delta()
    vj_delta = vj.put_delta()

    c1_delta = 0.5 * np.add((1 + beta) * xi_delta, (1 - beta) * vj_delta)  # crossover
    c2_delta = 0.5 * np.add((1 - beta) * xi_delta, (1 + beta) * vj_delta)

    # for i in range(N):  # crossover
    #     delta1 = 0.5 * ((1 + beta) * xi_delta[i] + (1 - beta) * vj_delta[i])
    #     delta2 = 0.5 * ((1 - beta) * xi_delta[i] + (1 + beta) * vj_delta[i])
    #     c1_delta.append(delta1)
    #     c2_delta.append(delta2)
    c1.get_delta(c1_delta)
    c1.get_fit()
    c1.get_feas()
    c2.get_delta(c2_delta)
    c2.get_fit()
    c2.get_feas()
    return select_better_fit(c1, c2)  # better crossover child


def DE(x_list):
    """
    DE algorithm
    :param x_list:
    :return: best x by DE
    """
    x_best = x_list[0]
    # DE
    t = 1
    while t <= T_DE:  # iteration of DE
        for i in range(N):  # iteration of generation
            u_best = X()
            for j in range(no):  # children of each node in each generation
                r_list = random.sample(range(N), 3)
                for m in range(len(r_list)):
                    while r_list[m] == i:
                        r_list[m] = random.randint(0, N - 1)
                vj = X()
                vj.get_delta(current_to_rand(x_list, r_list[0], r_list[1], r_list[2], i))
                vj.get_delta(compare_max(vj.put_delta()))
                vj.get_delta(compare_min(vj.put_delta()))
                vj.get_fit()
                vj.get_feas()

                # crossover
                cr_rand = random.random()
                if cr_rand <= CR:
                    uj = crossover_SBX(x_list[i], vj)
                else:
                    uj = x_list[i]

                # select
                if j == 1:
                    u_best = uj
                else:
                    u_best = select_better_fit(u_best, uj)
            if u_best.put_feas() <= x_list[i].put_feas() and u_best.put_feas() <= 0:
                x_list[i] = u_best
            if x_list[i].put_feas() < x_best.put_feas():
                x_best = x_list[i]

        t = t + 1
    return x_best


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


def SA(x_best):
    """
    SA algorithm
    :param x_best: best x from DE
    :return: best x after DESA
    """
    # initialize
    T = T_max
    x = x_best
    x_best_sa = x_best

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
            x_best_sa = x
        else:
            unfeasible_list.append(x)
            if len(unfeasible_list) == m:
                break
        T = a * T

    return x_best_sa


def main():
    print(A[..., 2])
    # initialize X
    x_list = np.empty([N], dtype=X)  # list of vectors
    for i in range(N):  # initialize x_list
        p = X()
        r_delta = np.array([random.uniform(0, 1) for _ in range(N)])
        p.get_delta(r_delta)
        p.get_fit()
        p.get_feas()
        x_list[i] = p

    # time count start
    time_start = time.time()

    # DE
    x_best_DE = DE(x_list)
    time_end_DE = time.time()
    # print(" DE:\n", x_best_DE.delta)
    print()
    print(" lowest cost by DE:", x_best_DE.put_fit())
    print()

    # SA
    x_best_DESA = SA(x_best_DE)
    time_end_SA = time.time()
    # print(" SA:\n", x_best_DESA.delta)
    print()

    # print times
    print(" time cost:")
    print(" DE :", time_end_DE - time_start)
    print(" SA :", time_end_SA - time_end_DE)
    print()

    # print best delta
    # for i in range(N):
    #     print(" the best vaccination rate of", i, "st node is", x_best_DESA.delta[i])

    # print lowest cost
    print()
    print(" the lowest cost of vaccination is", x_best_DESA.put_fit())


main()
