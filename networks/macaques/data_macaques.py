import numpy as np
import pathes

A = np.loadtxt(pathes.macaques_data)

Cn = np.loadtxt(pathes.macaques_cost)

gamma = np.loadtxt(pathes.macaques_curingrate)

Rou = np.loadtxt(pathes.macaques_rou)

with open(pathes.macaques_parameter) as f:
    lines = f.readlines()

N = int(lines[0])

E = int(lines[1])