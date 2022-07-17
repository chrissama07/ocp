import random
import math
import time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
import pathes
from networks.bundesliga import data_bundesliga

A = data_bundesliga.A

N = data_bundesliga.N  # number of nodes

E = data_bundesliga.E  # number of edges

Cn = data_bundesliga.Cn  # cost of each vaccine

gamma = data_bundesliga.gamma  # curing rate

Rou = data_bundesliga.Rou

first_delta = np.loadtxt(pathes.bundesliga_initial)

""":parameter for TS"""
T_TS = 100
d_TS = 0.0001
num_TS = 5

interval = 5
delta_list_TS = np.empty([T_TS // interval + 1])


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
            A[i, 2] = (1.0 - self.delta[int(A[i, 0])]) * (1.0 - self.delta[int(A[i, 1])]) * A[i, 2]

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


""" TS """

""":parameter TS lists"""
tabu_list = np.empty([N + 1], dtype=X)
can_N = np.zeros([num_TS], dtype=X)


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


def get_Can_N(x_now, tabu_num):
    this_delta = x_now.put_delta()
    t = 0
    while t < num_TS:
        while True:
            new_delta = np.zeros([N])
            for i in range(new_delta.size):  # generate new delta
                new_delta[i] = random.uniform(this_delta[i] - d_TS, this_delta[i] + d_TS)
            new_delta = compare_max(new_delta)
            new_delta = compare_min(new_delta)
            flag = 1
            for i in range(tabu_num):
                if (new_delta == tabu_list[i].put_fit()).all():
                    flag = 0
                    break
            if flag == 1:
                p = X()
                p.get_delta(new_delta)
                p.get_fit()
                p.get_feas()
                if p.put_feas() > 0:
                    continue
                can_N[t] = p
                break
        t += 1


def get_Xnew_TS():
    fit_max = np.zeros([can_N.size])
    for i in range(can_N.size):
        fit_max[i] = can_N[i].put_fit()
    j = fit_max.argmin()
    return can_N[j]


def TS():
    delta_list_TS[0] = tabu_list[0].put_fit()
    t = 0
    while t < T_TS:
        tabu_num = 1
        for i in range(tabu_list.size - 1):
            get_Can_N(tabu_list[i], tabu_num)
            tabu_list[i + 1] = get_Xnew_TS()
            tabu_num += 1
        fit_min = np.zeros([tabu_list.size])
        for i in range(tabu_list.size):
            fit_min[i] = tabu_list[i].put_fit()
        j = fit_min.argmin()
        tabu_list[0] = tabu_list[j]
        for i in range(1, tabu_list.size):
            tabu_list[i] = X()

        if t % interval == interval - 1:
            delta_list_TS[t // interval + 1] = tabu_list[0].put_fit()

        t += 1
    return tabu_list[0]


def main():
    p = X()
    p.get_delta(first_delta)
    p.get_fit()
    p.get_feas()
    tabu_list[0] = p
    # print(p.put_fit())
    # print(p.put_feas())

    # TS
    time_TS_start = time.time()
    x_bestTS = TS()
    time_TS_end = time.time()
    print(" lowest cost by TS:", x_bestTS.put_fit())
    # TS_fit = x_best_TS.put_fit()
    time_TS = time_TS_end - time_TS_start
    print("running time by TS is:", time_TS)
    np.savetxt(pathes.bundesliga_TS_output, delta_list_TS)


main()
