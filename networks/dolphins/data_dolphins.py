import numpy as np
import pathes

A = np.loadtxt(pathes.dolphins_data)

Cn = np.loadtxt(pathes.dolphins_cost)

gamma = np.loadtxt(pathes.dolphins_curingrate)

with open(pathes.dolphins_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])