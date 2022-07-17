import numpy as np
import pathes

A = np.loadtxt(pathes.highland_data)

Cn = np.loadtxt(pathes.highland_cost)

gamma = np.loadtxt(pathes.highland_curingrate)

Rou = np.loadtxt(pathes.highland_rou)

with open(pathes.highland_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])