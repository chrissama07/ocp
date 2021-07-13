import numpy as np
import pathes

A = np.loadtxt(pathes.household_data)

Cn = np.loadtxt(pathes.household_cost)

gamma = np.loadtxt(pathes.household_curingrate)

with open(pathes.household_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])