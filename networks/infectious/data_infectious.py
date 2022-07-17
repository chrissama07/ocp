import numpy as np
import pathes

A = np.loadtxt(pathes.infectious_data)

Cn = np.loadtxt(pathes.infectious_cost)

gamma = np.loadtxt(pathes.infectious_curingrate)

Rou = np.loadtxt(pathes.infectious_rou)

with open(pathes.infectious_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])