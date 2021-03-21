import random

a, b, c, d, e, f, g, h = range(8)

A = [
    [0, random.uniform(0.5, 0.8), random.uniform(0.5, 0.8), random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8), 0,
     0],
    [random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8), 0, 0, 0, 0, 0],
    [random.uniform(0.5, 0.8), random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8), 0,
     0],
    [random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8),
     random.uniform(0.5, 0.8)],
    [0, 0, 0, random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8), 0, 0],
    [random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8), 0, random.uniform(0.5, 0.8), 0, 0],
    [0, 0, 0, random.uniform(0.5, 0.8), 0, 0, 0, random.uniform(0.5, 0.8)],
    [0, 0, 0, random.uniform(0.5, 0.8), 0, 0, random.uniform(0.5, 0.8), 0]
]

N = 8

Cn = [random.randint(10, 20) for _ in range(N)]

no = 5
CR = 0.7
T_DE = 20
gamma = 0.6


def fitness_value(delta):
    sum = 0
    for i in range(N):
        sum += delta[i] * Cn[i]
    return sum


class X:
    delta = []
    fit = 0

    def __init__(self):
        self.delta = [random.uniform(0, 1) for _ in range(N)]
        self.fit = fitness_value(self.delta)


x_list = []
for i in range(N):
    p = X()
    x_list.append(p)
