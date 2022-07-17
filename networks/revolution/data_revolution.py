import numpy as np
import pathes

A = np.loadtxt(pathes.revolution_data)

Cn = np.loadtxt(pathes.revolution_cost)

gamma = np.loadtxt(pathes.revolution_curingrate)

Rou = np.loadtxt(pathes.revolution_rou)

with open(pathes.revolution_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])