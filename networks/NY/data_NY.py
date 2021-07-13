import numpy as np
import pathes

A = np.loadtxt(pathes.NY_data)

Cn = np.loadtxt(pathes.NY_cost)

gamma = np.loadtxt(pathes.NY_curingrate)

with open(pathes.NY_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])