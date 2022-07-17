import numpy as np
import pathes

A = np.loadtxt(pathes.hiv_data)

Cn = np.loadtxt(pathes.hiv_cost)

gamma = np.loadtxt(pathes.hiv_curingrate)

Rou = np.loadtxt(pathes.hiv_rou)

with open(pathes.hiv_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])