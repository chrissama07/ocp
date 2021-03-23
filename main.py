import random
import numpy as np

a, b, c, d, e, f, g, h = range(8)  # nodes

beta_min = 0.5
beta_max = 0.8

A = ([  # adjacency matrix of infection rate
    [0, random.uniform(beta_min, beta_max), random.uniform(beta_min, beta_max), random.uniform(beta_min, beta_max), 0,
     random.uniform(beta_min, beta_max), 0,
     0],
    [random.uniform(beta_min, beta_max), 0, random.uniform(beta_min, beta_max), 0, 0, 0, 0, 0],
    [random.uniform(beta_min, beta_max), random.uniform(beta_min, beta_max), 0, random.uniform(beta_min, beta_max), 0,
     random.uniform(beta_min, beta_max), 0,
     0],
    [random.uniform(beta_min, beta_max), 0, random.uniform(beta_min, beta_max), 0, random.uniform(beta_min, beta_max),
     0, random.uniform(beta_min, beta_max),
     random.uniform(beta_min, beta_max)],
    [0, 0, 0, random.uniform(beta_min, beta_max), 0, random.uniform(beta_min, beta_max), 0, 0],
    [random.uniform(beta_min, beta_max), 0, random.uniform(beta_min, beta_max), 0, random.uniform(beta_min, beta_max),
     0, 0, 0],
    [0, 0, 0, random.uniform(beta_min, beta_max), 0, 0, 0, random.uniform(beta_min, beta_max)],
    [0, 0, 0, random.uniform(beta_min, beta_max), 0, 0, random.uniform(beta_min, beta_max), 0]
])

N = 8  # number of nodes

Cn = [random.randint(10, 20) for _ in range(N)]  # the cost of vaccine

no = 5  # number of nodes generated by each node
CR = 0.7  # rate of crossover
T_DE = 20  # iteration of DE
gamma = [random.uniform(0.6, 0.7) for _ in range(N)]  # curing rate

""":parameter k and F: for current/rand/1"""
k = 0.5
F = 0.8

""":parameter for crossoverSBX"""
sbx_n = 1.1


# class of X
class X:
    delta = []
    fit = 0
    feas = 0

    def fitness_value(self):
        """
        calculate fitness_value
        :param self:   list of vaccination rate
        :return:    fitness value
        """

        fitness = 0
        for i in range(N):
            fitness += self.delta[i] * Cn[i]
        return fitness

    def feasible_value(self):
        """
        calculate feasible value
        :return: feasible value
        """
        A_ = np.zeros([N, N])
        for i in range(N):
            for j in range(N):
                if A[i][j] != 0:
                    A_[i][j] = (1.0 - self.delta[i]) * (1.0 - self.delta[j]) * A[i][j]
        return max(np.linalg.eigvals(A_ - np.diag(gamma)))

    def get_fit(self):
        self.fit = 0
        for i in range(N):
            self.fit += self.delta[i] * Cn[i]

    def get_feas(self):
        self.feas = self.feasible_value()

    def get_delta(self, delta):
        self.delta = delta

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
    v_delta = []
    for j in range(N):
        current_delta = xx_list[i].delta[j] + \
                        k * (xx_list[r1].delta[j] - xx_list[i].delta[j]) + \
                        F * (xx_list[r2].delta[j] - xx_list[r3].delta[j])
        v_delta.append(current_delta)
    return v_delta


def compare_max(delta):
    '''
    lower bound
    :param delta: delta
    :return: turn into lower bound delta
    '''
    for i in range(len(delta)):
        delta[i] = max(delta[i], beta_min)
    return delta


def compare_min(delta):
    """
    upper bound
    :param delta: delta
    :return: turn into upper bound delta
    """
    for i in range(len(delta)):
        delta[i] = min(delta[i], beta_max)
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
    belta = 0
    while isinstance(belta, complex):   # belt must not be complex
        sbx_rand = random.random()
        if sbx_rand <= 0.5:
            belta = (2 * sbx_rand) ** (1 / (1 + sbx_n))
        else:
            belta = (1 / (2 - sbx_n * 2)) ** (1 / (1 + sbx_n))
    c1 = X()
    c2 = X()
    c1_delta = []
    c2_delta = []
    xi_delta = xi.put_delta()
    vj_delta = vj.put_delta()
    for i in range(N):      # crossover
        delta1 = 0.5 * ((1 + belta) * xi_delta[i] + (1 - belta) * vj_delta[i])
        delta2 = 0.5 * ((1 - belta) * xi_delta[i] + (1 + belta) * vj_delta[i])
        c1_delta.append(delta1)
        c2_delta.append(delta2)
    c1.get_delta(c1_delta)
    c1.get_fit()
    c1.get_feas()
    c2.get_delta(c2_delta)
    c2.get_fit()
    c2.get_feas()
    return select_better_fit(c1, c2)    # better crossover child

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


def main():
    # initialize X
    x_list = []  # list of vectors
    for i in range(N):  # initialize x_list
        p = X()
        r_delta = [random.uniform(0, 1) for _ in range(N)]
        p.get_delta(r_delta)
        p.get_fit()
        p.get_feas()
        x_list.append(p)
        # print(x_list[i].delta)
        # print(x_list[i].fit)
        # print(x_list[i].feas)

    # DE
    x_best = DE(x_list)
    print(x_best.delta)


main()
