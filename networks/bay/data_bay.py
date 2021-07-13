import numpy as np
import cupy as cp

import pathes

A = np.loadtxt(pathes.bay_data)

Cn = np.loadtxt(pathes.bay_cost)

gamma = np.loadtxt(pathes.bay_curingrate)

with open(pathes.bay_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])

A = cp.asarray(A)

Cn = cp.asarray(Cn)

gamma = cp.asarray(gamma)

a = cp.sum(A)
