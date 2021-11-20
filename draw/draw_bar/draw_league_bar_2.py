import numpy as np
import matplotlib.pyplot as plt
import pathes
from draw import draw_pathes

name_list = ['DESA', 'SA', 'TS']
# 柱高信息
Y = [0]
Y1 = [0]
Y2 = [0]

with open(pathes.league_output) as f:
    lines = f.readlines()
lines.pop(0)
lines = np.array(lines)
numbers = [float(i) for i in lines[1].split()]
Y[0] = numbers[2]

npsai = np.loadtxt(pathes.league_SA_output)
nptsi = np.loadtxt(pathes.league_TS_output)

Y1[0] = npsai[npsai.size - 1]
Y2[0] = nptsi[nptsi.size - 1]

X = [0]
X1 = [1]
X2 = [2]

total_width, n = 0.6, 2
width = total_width / n

fig = plt.figure(figsize=(9, 7))

plt.title('Algorithm Comparison of Sexual Escorts', size=20)

plt.bar(X, Y, width=0.5, label='DESA', fc='deepskyblue')
plt.bar(X1, Y1, width=0.5, label='SA', fc='lightpink')
plt.bar(X2, Y2, width=0.5, label='TS', fc='darkseagreen')
plt.legend()
plt.xlabel('Different Algorithm', size=15)
plt.ylabel('Lowest cost of vaccination', size=15)
plt.ylim(100, 160)
plt.xlim(-1, 3)
plt.savefig(draw_pathes.league_pictures_bar_2)

plt.show()

