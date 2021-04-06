import numpy as np

A = np.loadtxt("iceland.data.txt")

Cn = np.loadtxt("iceland.cost.txt")

gamma = np.loadtxt("iceland.curingrate.txt")

with open(r'networks/iceland/iceland.parameter.txt') as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])