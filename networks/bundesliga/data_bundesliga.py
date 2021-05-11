import numpy as np
import pathes

A = np.loadtxt(pathes.bundesliga_data)

Cn = np.loadtxt(pathes.bundesliga_cost)

gamma = np.loadtxt(pathes.bundesliga_curingrate)

with open(pathes.bundesliga_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])