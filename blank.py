import numpy as np
import random
import pathes
from scipy import sparse
from scipy.sparse.linalg import eigsh
# from networks.league import data_league
# from networks.bundesliga import data_bundesliga
# from networks.highland import data_highland
# from networks.highschool import data_highschool
# from networks.hiv import data_hiv
# import data_iceland
# from networks.macaques import data_macaques
# from networks.revolution import data_revolution
# from networks.windsurfers import data_windsurfers
from networks.zachary import data_zachary

A = data_zachary.A

N = data_zachary.N  # number of nodes

E = data_zachary.E  # number of edges

Cn = data_zachary.Cn  # cost of each vaccine

gamma = data_zachary.gamma  # curing rate


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


def main():
    p = X()
    while 1:
        r_delta = np.array([random.uniform(0, 1) for _ in range(N)])
        p.get_delta(r_delta)
        p.get_fit()
        fit = p.put_fit()
        if fit > 300:
            break
    print(fit)
    with open(pathes.zachary_blank_output, "w") as f:
        f.write(str(fit) + "\n")
    f.close()


main()
