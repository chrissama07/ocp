import numpy as np
import matplotlib.pyplot as plt
import pathes
from draw import draw_pathes

name_list = ['current_to_rand', 'rand2', 'rand_to_best', 'current_to_best', 'no_crossover']
# 柱高信息
Y = [0, 0, 0, 0, 0]
Y1 = [0, 0, 0, 0, 0]

with open(pathes.highland_output) as f:
    lines = f.readlines()

i = 0
lines.pop(0)
lines = np.array(lines)
for line in lines:
    numbers = [float(i) for i in line.split()]
    Y[i] = numbers[1]
    Y1[i] = numbers[2]
    i += 1

X = list(range(len(Y)))

total_width, n = 0.6, 2
width = total_width / n

fig=plt.figure(figsize=(9, 7))

plt.title('highland', size=20)

plt.ylim(int(min(Y1)), int(max(Y) + 1))
# plt.yticks(range(int(min(Y1)), int(max(Y) + 3), 1))

plt.bar(X, Y, width=width, label='DE', tick_label=name_list, fc='indigo')
for i in range(len(X)):
    X[i] = X[i] + width
plt.bar(X, Y1, width=width, label='DESA', tick_label=name_list, fc='r')
plt.legend()
plt.xlabel('Different Strategy', size=15)
plt.ylabel('Objective function value', size=15)

plt.savefig(draw_pathes.highland_pictures_bar_1)

plt.show()

