import random
import math
import time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
import pathes
from networks.hiv import data_hiv

A = data_hiv.A

N = data_hiv.N  # number of nodes

E = data_hiv.E  # number of edges

Cn = data_hiv.Cn  # cost of each vaccine

gamma = data_hiv.gamma  # curing rate

Rou = data_hiv.Rou  # vaccination rate

first_delta = np.loadtxt(pathes.hiv_initial)

""":parameter: for GSK"""
T_GSK = 100
GSK_p = 0.1
k_f = 0.01   # 0.5
k_r = 0.1   # 0.9
K = 10

""":parameter for crossoverSBX"""
sbx_n = 10

interval = 5
delta_list_GSK = np.empty([T_GSK // interval + 1])


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
        """calculate feasible value
        :return: feasible value
        """
        # A_ = np.zeros([N, N])
        # for i in range(N):
        #     for j in range(N):
        #         if A[i][j] != 0:
        #             A_[i][j] = (1.0 - self.delta[i]) * (1.0 - self.delta[j]) * A[i][j]
        # return max(np.linalg.eigvals(A_ - np.diag(gamma)))
        # TODO:
        for i in range(E):
            A[i, 2] = (1.0 - self.delta[int(A[i, 0])] * Rou[int(A[i, 0])]) * (1.0 - self.delta[int(A[i, 1])] * Rou[int(A[i, 0])]) * A[i, 2]

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


def index_of_X_best(xx_list):
    index = 0
    min_fit = 1
    for i in range(len(xx_list)):
        if xx_list[i].put_fit() < min_fit:
            index = i
            min_fit = xx_list[i].put_fit()
    return index


def index_of_X_worst(xx_list):
    index = 0
    max_fit = 0
    for i in range(len(xx_list)):
        if xx_list[i].put_fit() > max_fit:
            index = i
            max_fit = xx_list[i].put_fit()
    return index


def junior(xx_list, r, i):
    if random.uniform(0, 1) <= k_r:
        if xx_list[i].put_fit() > xx_list[r].put_fit():
            v_delta = np.add(xx_list[i].delta,
                             k_f * np.add(np.subtract(xx_list[max(0, i - 1)].delta, xx_list[min(N - 1, i + 1)].delta),
                                          np.subtract(xx_list[r].delta, xx_list[i].delta)))
        else:
            v_delta = np.add(xx_list[i].delta,
                             k_f * np.add(np.subtract(xx_list[max(0, i - 1)].delta, xx_list[min(N - 1, i + 1)].delta),
                                          np.subtract(xx_list[i].delta, xx_list[r].delta)))
    else:
        v_delta = xx_list[i].delta
    return v_delta


def senior(xx_list, i, D_junior):
    if random.uniform(0, 1) <= k_r:
        D_senior = N - D_junior
        NP = int(D_senior * GSK_p)
        r_list = random.randint(D_junior - 1 + NP * 2, N - 1)
        x_p_worst = xx_list[index_of_X_worst(xx_list[D_junior - 1 + NP: D_junior - 1 + NP * 2 - 1])]
        x_p_best = xx_list[index_of_X_best(xx_list[D_junior - 1: D_junior - 1 + NP - 1])]
        if xx_list[i].put_fit() > xx_list[r_list].put_fit():
            v_delta = np.add(xx_list[i].delta,
                             k_f * np.add(np.subtract(x_p_best.delta, x_p_worst.delta),
                                          np.subtract(xx_list[r_list].delta, xx_list[i].delta)))
        else:
            v_delta = np.add(xx_list[i].delta,
                             k_f * np.add(np.subtract(x_p_best.delta, x_p_worst.delta),
                                          np.subtract(xx_list[i].delta, xx_list[r_list].delta)))
    else:
        v_delta = xx_list[i].delta
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


def GSK(x_list):
    """
    DE algorithm
    :param x_list:
    :return: best x by DE
    """
    x_best = x_list[0]
    # DE
    G = 0

    # delta_list_GSK[0] = x_best.put_fit()

    print(x_best.put_fit())

    while G <= T_GSK:  # iteration of DE
        D_junior = int(N * pow((1 - G / T_GSK), K))

        for i in range(N):  # iteration of generation

            u_best = X()
            for j in range(N):
                vj = X()
                r = random.randint(0, N - 1)
                if j <= D_junior:
                    vj.get_delta(junior(x_list, r, j))
                else:
                    vj.get_delta(senior(x_list, j, D_junior))

                vj.get_delta(compare_max(vj.put_delta()))
                vj.get_delta(compare_min(vj.put_delta()))
                vj.get_fit()
                vj.get_feas()

                if j == 0:
                    u_best = vj
                else:
                    u_best = select_better_fit(u_best, vj)

            if u_best.put_fit() <= x_list[i].put_fit() and u_best.put_feas() <= 0:
                x_list[i] = u_best
            if x_list[i].put_fit() < x_best.put_fit() and x_list[i].put_feas() <= 0:
                x_best = x_list[i]

        if G % interval == interval - 1:
            delta_list_GSK[G // interval + 1] = x_best.put_fit()

        G = G + 1

    return x_best


def main():

    x = X()
    x.get_delta(first_delta)
    x.get_fit()
    x.get_feas()
    # blank fit
    # print("blank fit:", blank_fit)
    delta_list_GSK[0] = x.put_fit()
    print(x.put_fit())
    # GSK
    x_list = np.empty([N], dtype=X)
    x_list[0] = x

    for i in range(N - 1):
        p = X()
        r_delta = np.array([random.uniform(0, 1) for _ in range(N)])
        p.get_delta(r_delta)
        p.get_fit()
        p.get_feas()
        x_list[i + 1] = p

    time_GSK_start = time.time()
    x_best_DE_GSK = GSK(x_list)
    print(" lowest cost by GSK:", x_best_DE_GSK.put_fit())
    print(x_best_DE_GSK.delta)
    DE_GSK_fit = x_best_DE_GSK.put_fit()
    time_GSK_end = time.time()
    DE_GSK_time = time_GSK_end - time_GSK_start

    print("running time by GSK is:", DE_GSK_time)

    np.savetxt(pathes.hiv_GSK, delta_list_GSK)


main()
