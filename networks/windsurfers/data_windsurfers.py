import numpy as np
import pathes

A = np.loadtxt(pathes.windsurfers_data)

Cn = np.loadtxt(pathes.windsurfers_cost)

gamma = np.loadtxt(pathes.windsurfers_curingrate)

Rou = np.loadtxt(pathes.windsurfers_rou)

with open(pathes.windsurfers_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])