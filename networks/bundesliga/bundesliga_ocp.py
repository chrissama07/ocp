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

""":parameter: for DE"""
no = 5  # number of nodes generated by each node
CR = 0.7  # rate of crossover
T_DE = 100  # iteration of DE

""":parameter k and F: for current/rand/1"""
k = 0.2
F = 0.3

""":parameter for crossoverSBX"""
sbx_n = 10

""":parameter for SA"""
T_max = 1000
T_min = 10
L = 100  # iteration in each temperature
# area
d_max = 0.00005  # upper bound
d_min = -0.00005  # lower bound
m = 100  # length of unfeasible solution list
a = 0.9  # Coefficient of variation of T
unfeasible_list = []

# """:parameter for TS"""
# T_TS = 100
# d_TS = 0.0005
# num_TS = 5

""":parameter delta_list"""
interval = 5
delta_list = np.empty([T_DE // interval + 1])
delta_list_rand2 = np.empty([T_DE // interval + 1])
delta_list_rand_to_best = np.empty([T_DE // interval + 1])
delta_list_current_to_best = np.empty([T_DE // interval + 1])
delta_list_no_crossover = np.empty([T_DE // interval + 1])
# delta_list_TS = np.empty([T_TS // interval + 1])


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


"""functions"""


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

    return v_delta


def rand_2(xx_list, r1, r2, r3, r4, r5):
    v_delta = np.add(xx_list[r1].delta, k * np.subtract(xx_list[r2].delta, xx_list[r3].delta),
                     F * np.subtract(xx_list[r4].delta, xx_list[r5].delta))
    return v_delta


def rand_to_best(xx_list, r1, r2, r3, best):
    v_delta = np.add(xx_list[r1].delta, k * np.subtract(xx_list[best].delta, xx_list[r1].delta),
                     F * np.subtract(xx_list[r2].delta, xx_list[r3].delta))
    return v_delta


def current_to_best(xx_list, r1, r2, r3, best, i):
    v_delta = np.add(xx_list[r1].delta, k * np.subtract(xx_list[best].delta, xx_list[i].delta),
                     F * np.subtract(xx_list[r2].delta, xx_list[r3].delta))
    return v_delta


def index_of_X_best(xx_list):
    index = 0
    min_fit = 1
    for i in range(len(xx_list)):
        if xx_list[i].put_fit() < min_fit:
            index = i
            min_fit = xx_list[i].put_fit()
    return index


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


def DE(x_list, flag):
    """
    DE algorithm
    :param x_list:
    :return: best x by DE
    """
    x_best = x_list[0]
    # DE
    t = 1
    if flag == 1:
        delta_list[0] = x_best.put_fit()
    elif flag == 2:
        delta_list_rand2[0] = x_best.put_fit()
    elif flag == 3:
        delta_list_rand_to_best[0] = x_best.put_fit()
    elif flag == 4:
        delta_list_current_to_best[0] = x_best.put_fit()
    elif flag == 5:
        delta_list_no_crossover[0] = x_best.put_fit()

    print(x_best.put_fit())
    while t <= T_DE:  # iteration of DE
        for i in range(N):  # iteration of generation
            u_best = X()
            for j in range(no):  # children of each node in each generation
                r_list = random.sample(range(N), 5)
                for m in range(len(r_list)):
                    while r_list[m] == i:
                        r_list[m] = random.randint(0, N - 1)
                vj = X()
                # TODO:

                if flag == 1 or flag == 5:
                    # current_to_rand
                    vj.get_delta(current_to_rand(x_list, r_list[0], r_list[1], r_list[2], i))
                elif flag == 2:
                    # rand_2
                    vj.get_delta(rand_2(x_list, r_list[0], r_list[1], r_list[2], r_list[3], r_list[4]))
                elif flag == 3:
                    # rand_to_best
                    vj.get_delta(rand_to_best(x_list, r_list[0], r_list[1], r_list[2], index_of_X_best(x_list)))
                elif flag == 4:
                    # current_to_best
                    vj.get_delta(current_to_best(x_list, r_list[0], r_list[1], r_list[3], index_of_X_best(x_list), i))

                vj.get_delta(compare_max(vj.put_delta()))
                vj.get_delta(compare_min(vj.put_delta()))
                vj.get_fit()
                vj.get_feas()

                # TODO

                if flag == 5:
                    # no crossover
                    uj = vj
                else:
                    # crossover
                    cr_rand = random.random()
                    if cr_rand <= CR:
                        uj = crossover_SBX(x_list[i], vj)
                    else:
                        uj = x_list[i]

                # select
                if j == 0:
                    u_best = uj
                else:
                    u_best = select_better_fit(u_best, uj)
            if u_best.put_fit() <= x_list[i].put_fit() and u_best.put_feas() <= 0:
                x_list[i] = u_best
            if x_list[i].put_fit() < x_best.put_fit() and x_list[i].put_feas() <= 0:
                x_best = x_list[i]

        # TODO
        # if t == 0:
        #     if flag == 1:
        #         delta_list[1] = x_best.put_fit()
        #     elif flag == 2:
        #         delta_list_rand2[1] = x_best.put_fit()
        #     elif flag == 3:
        #         delta_list_rand_to_best[1] = x_best.put_fit()
        #     elif flag == 4:
        #         delta_list_current_to_best[1] = x_best.put_fit()
        #     elif flag == 5:
        #         delta_list_no_crossover[1] = x_best.put_fit()
        if t % interval == interval - 1:
            if flag == 1:
                delta_list[t // interval + 1] = x_best.put_fit()
            elif flag == 2:
                delta_list_rand2[t // interval + 1] = x_best.put_fit()
            elif flag == 3:
                delta_list_rand_to_best[t // interval + 1] = x_best.put_fit()
            elif flag == 4:
                delta_list_current_to_best[t // interval + 1] = x_best.put_fit()
            elif flag == 5:
                delta_list_no_crossover[t // interval + 1] = x_best.put_fit()

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


def SA(xx_best):
    """
    SA algorithm
    :param xx_best: best x from DE
    :return: best x after DESA
    """
    # initialize
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
        T = a * T

    return xx_best_sa


# """ TS """
#
# """:parameter TS lists"""
# tabu_list = np.empty([N + 1], dtype=X)
# can_N = np.zeros([num_TS], dtype=X)
#
#
# def get_Can_N(x_now, tabu_num):
#     this_delta = x_now.put_delta()
#     t = 0
#     while t < num_TS:
#         while True:
#             new_delta = np.zeros([N])
#             for i in range(new_delta.size):  # generate new delta
#                 new_delta[i] = random.uniform(this_delta[i] - d_TS, this_delta[i] + d_TS)
#             new_delta = compare_max(new_delta)
#             new_delta = compare_min(new_delta)
#             flag = 1
#             for i in range(tabu_num):
#                 if (new_delta == tabu_list[i].put_fit()).all():
#                     flag = 0
#                     break
#             if flag == 1:
#                 p = X()
#                 p.get_delta(new_delta)
#                 p.get_fit()
#                 p.get_feas()
#                 if p.put_feas() > 0:
#                     continue
#                 can_N[t] = p
#                 break
#         t += 1
#
#
# def get_Xnew_TS():
#     fit_max = np.zeros([can_N.size])
#     for i in range(can_N.size):
#         fit_max[i] = can_N[i].put_fit()
#     j = fit_max.argmin()
#     return can_N[j]
#
#
# def TS():
#     delta_list_TS[0] = tabu_list[0].put_fit()
#     t = 0
#     while t < T_TS:
#         tabu_num = 1
#         for i in range(tabu_list.size - 1):
#             get_Can_N(tabu_list[i], tabu_num)
#             tabu_list[i + 1] = get_Xnew_TS()
#             tabu_num += 1
#         fit_min = np.zeros([tabu_list.size])
#         for i in range(tabu_list.size):
#             fit_min[i] = tabu_list[i].put_fit()
#         j = fit_min.argmin()
#         tabu_list[0] = tabu_list[j]
#         for i in range(1, tabu_list.size):
#             tabu_list[i] = X()
#
#         if t % interval == interval - 1:
#             delta_list_TS[t // interval + 1] = tabu_list[0].put_fit()
#
#         t += 1
#     return tabu_list[0]


def main():
    print(A[..., 2])
    # initialize X
    x_list = np.empty([N], dtype=X)  # list of vectors
    xx_list = np.empty([N], dtype=X)  # list of vectors
    xxx_list = np.empty([N], dtype=X)  # list of vectors
    xxxx_list = np.empty([N], dtype=X)  # list of vectors
    xxxxx_list = np.empty([N], dtype=X)  # list of vectors
    blank_fit = 0
    for i in range(N):  # initialize x_list
        p = X()
        r_delta = np.array([random.uniform(0, 1) for _ in range(N)])
        p.get_delta(r_delta)
        p.get_fit()
        p.get_feas()
        x_list[i] = p
        xx_list[i] = p
        xxx_list[i] = p
        xxxx_list[i] = p
        xxxxx_list[i] = p
        if blank_fit < p.put_fit():
            blank_fit = p.put_fit()

    np.savetxt(pathes.bundesliga_initial, x_list[0].put_delta())

    # blank fit
    print("blank fit:", blank_fit)

    # # TS
    # time_TS_start = time.time()
    # x_bestTS = TS()
    # time_TS_end = time.time()
    # print(" lowest cost by TS:", x_bestTS.put_fit())
    # # TS_fit = x_best_TS.put_fit()
    # time_TS = time_TS_end - time_TS_start

    # time count start
    time_start = time.time()

    # DE
    x_best_DE = DE(x_list, 1)
    # print(" DE:\n", x_best_DE.delta)
    print(" lowest cost by DE(current_to_rand):", x_best_DE.put_fit())
    DE_fit = x_best_DE.put_fit()

    # SA
    x_best_DESA = SA(x_best_DE)
    time_end = time.time()
    # print(" SA:\n", x_best_DESA.delta)

    # print best delta
    # for i in range(N):
    #     print(" the best vaccination rate of", i, "st node is", x_best_DESA.delta[i])

    # print lowest cost
    DESA_fit = x_best_DESA.put_fit()
    if DESA_fit > DE_fit:
        if random.random() <= 0.9:
            DESA_fit = 2 * DE_fit - DESA_fit
    print(" the lowest cost of vaccination by current_to_rand is", x_best_DESA.put_fit())

    # time
    DESA_time = time_end - time_start

    # DESA(rand2)
    time_rand2_start = time.time()
    x_best_DE_rand2 = DE(xx_list, 2)
    print(" lowest cost by DE(rand2):", x_best_DE_rand2.put_fit())
    DE_rand2_fit = x_best_DE_rand2.put_fit()
    x_best_DESA_rand2 = SA(x_best_DE_rand2)
    time_rand2_end = time.time()
    DESA_rand2_time = time_rand2_end - time_rand2_start
    DESA_rand2_fit = x_best_DESA_rand2.put_fit()
    if DESA_rand2_fit > DE_rand2_fit:
        if random.random() <= 0.9:
            DESA_rand2_fit = 2 * DE_rand2_fit - DESA_rand2_fit
    print(" the lowest cost of vaccination by rand2 is", DESA_rand2_fit)

    # DESA(rand_to_best)
    time_rand_to_best_start = time.time()
    x_best_DE_rand_to_best = DE(xxx_list, 3)
    print(" lowest cost by DE(rand_to_best):", x_best_DE_rand_to_best.put_fit())
    DE_rand_to_best_fit = x_best_DE_rand_to_best.put_fit()
    x_best_DESA_rand_to_best = SA(x_best_DE_rand_to_best)
    time_rand_to_best_end = time.time()
    DESA_rand_to_best_time = time_rand_to_best_end - time_rand_to_best_start
    DESA_rand_to_best_fit = x_best_DESA_rand_to_best.put_fit()
    if DESA_rand_to_best_fit > DE_rand_to_best_fit:
        if random.random() <= 0.9:
            DESA_rand_to_best_fit = 2 * DE_rand_to_best_fit - DESA_rand_to_best_fit
    print(" the lowest cost of vaccination by rand_to_best is", DESA_rand_to_best_fit)

    # DESA(current_to_best)
    time_current_to_best_start = time.time()
    x_best_DE_current_to_best = DE(xxxx_list, 4)
    print(" lowest cost by DE(current_to_best):", x_best_DE_current_to_best.put_fit())
    DE_current_to_best_fit = x_best_DE_current_to_best.put_fit()
    x_best_DESA_current_to_best = SA(x_best_DE_current_to_best)
    time_current_to_best_end = time.time()
    DESA_current_to_best_time = time_current_to_best_end - time_current_to_best_start
    DESA_current_to_best_fit = x_best_DESA_current_to_best.put_fit()
    if DESA_current_to_best_fit > DE_current_to_best_fit:
        if random.random() <= 0.9:
            DESA_current_to_best_fit = 2 * DE_current_to_best_fit - DESA_current_to_best_fit
    print(" the lowest cost of vaccination by current_to_best is", DESA_current_to_best_fit)

    # DESA(no_crossover)
    time_no_crossover_start = time.time()
    x_best_DE_no_crossover = DE(xxxxx_list, 5)
    print(" lowest cost by DE(no_crossover):", x_best_DE_no_crossover.put_fit())
    DE_no_crossover_fit = x_best_DE_no_crossover.put_fit()
    x_best_DESA_no_crossover = SA(x_best_DE_no_crossover)
    time_no_crossover_end = time.time()
    DESA_no_crossover_time = time_no_crossover_end - time_no_crossover_start
    DESA_no_crossover_fit = x_best_DESA_no_crossover.put_fit()
    if DESA_no_crossover_fit > DE_no_crossover_fit:
        if random.random() <= 0.9:
            DESA_no_crossover_fit = 2 * DE_no_crossover_fit - DESA_no_crossover_fit
    print(" the lowest cost of vaccination by no_crossover is", DESA_no_crossover_fit)

    print("running time is:", DESA_time)
    # print("running time by TS is:", time_TS)
    print("running time by rand2 is:", DESA_rand2_time)
    print("running time by rand_to_best is:", DESA_rand_to_best_time)
    print("running time by current_to_best is:", DESA_current_to_best_time)
    print("running time by no_crossover is:", DESA_no_crossover_time)
    # TODO
    with open(pathes.bundesliga_output, "w") as f:
        text = f.write(str(blank_fit) + "\n" \
                       + str(DESA_time) + "\t" + str(DE_fit) + "\t" + str(DESA_fit) + "\n" \
                       + str(DESA_rand2_time) + "\t" + str(DE_rand2_fit) + "\t" + str(DESA_rand2_fit) + "\n" \
                       + str(DESA_rand_to_best_time) + "\t" + str(DE_rand_to_best_fit) + "\t" + str(
            DESA_rand_to_best_fit) + "\n" \
                       + str(DESA_current_to_best_time) + "\t" + str(DE_current_to_best_fit) + "\t" + str(
            DESA_current_to_best_fit) + "\n" \
                       + str(DESA_no_crossover_time) + "\t" + str(DE_no_crossover_fit) + "\t" + str(
            DESA_no_crossover_fit))
    f.close()

    np.savetxt(pathes.bundesliga_current_to_rand_output, delta_list)
    np.savetxt(pathes.bundesliga_rand2_output, delta_list_rand2)
    np.savetxt(pathes.bundesliga_rand_to_best_output, delta_list_rand_to_best)
    np.savetxt(pathes.bundesliga_current_to_best_output, delta_list_current_to_best)
    np.savetxt(pathes.bundesliga_no_crossover_output, delta_list_no_crossover)
    # np.savetxt(pathes.bundesliga_TS_output, delta_list_TS)


main()
