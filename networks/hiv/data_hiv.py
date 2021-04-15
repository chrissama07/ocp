import numpy as np
import pathes

A = np.loadtxt(pathes.hiv_data)

Cn = np.loadtxt(pathes.hiv_cost)

gamma = np.loadtxt(pathes.hiv_curingrate)

with open(pathes.hiv_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])