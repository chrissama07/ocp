import numpy as np
import matplotlib.pyplot as plt
import pathes
from draw import draw_pathes

name_list = ['current_to_rand', 'rand2', 'rand_to_best', 'current_to_best', 'no_crossover', 'mms', 'immsade', 'agde-mutation']
# 柱高信息
Y = [0, 0, 0, 0, 0, 0, 0, 0]
Y1 = [0, 0, 0, 0, 0, 0, 0, 0]

with open(pathes.bundesliga_output) as f:
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

fig=plt.figure(figsize=(12, 7))

ax1 = fig.add_subplot(2, 1, 1)

plt.title('Hamsterster', size=20)

plt.ylim(int(min(Y1)), int(max(Y) + 1))
# plt.yticks(range(int(min(Y1)), int(max(Y) + 3), 1))

ax1.bar(X, Y, width=width, label='DE', fc='indigo')
for i in range(len(X)):
    X[i] = X[i] + width
ax1.bar(X, Y1, width=width, label='DESA', fc='r')
plt.legend()
# plt.ylabel('Lowest cost of vaccination', size=15)

ax2 = fig.add_subplot(2, 1, 2)
ax2.bar(X, Y, width=width, label='DE', tick_label=name_list, fc='indigo')
for i in range(len(X)):
    X[i] = X[i] + width
ax2.bar(X, Y1, width=width, label='DESA', tick_label=name_list, fc='r')
plt.xlabel('Contrast in Different Strategies', size=15)
ax2.set_ylabel('Lowest cost of vaccination', size=15)
ax2.yaxis.set_label_coords(-0.1, 1)

ax1.set_ylim(2192, 2205)
ax2.set_ylim(1967.5, 1976)
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop='off')
ax2.xaxis.tick_bottom()
d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal


plt.savefig(draw_pathes.bundesliga_pictures_bar_1)

plt.show()

