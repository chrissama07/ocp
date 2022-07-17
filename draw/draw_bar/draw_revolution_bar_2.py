import numpy as np
import matplotlib.pyplot as plt
import pathes
from draw import draw_pathes

name_list = ['DESA', 'SA', 'TS', 'AGDE', 'GSK']
# 柱高信息
Y = [0]
Y1 = [0]
Y2 = [0]
Y3 = [0]
Y4 = [0]

with open(pathes.revolution_output) as f:
    lines = f.readlines()
lines.pop(0)
lines = np.array(lines)
numbers = [float(i) for i in lines[5].split()]
Y[0] = numbers[2] * 100

npsai = np.loadtxt(pathes.revolution_SA_output)
nptsi = np.loadtxt(pathes.revolution_TS_output)
npagdei = np.loadtxt(pathes.revolution_agde_algorithm)
npgski = np.loadtxt(pathes.revolution_GSK)

Y1[0] = npsai[npsai.size - 1] * 100
Y2[0] = nptsi[nptsi.size - 1] * 100
Y3[0] = npagdei[npagdei.size - 1] * 100
Y4[0] = npgski[npgski.size - 1] * 100

X = name_list[0]
X1 = name_list[1]
X2 = name_list[2]
X3 = name_list[3]
X4 = name_list[4]

total_width, n = 0.6, 2
width = total_width / n

fig = plt.figure(figsize=(9, 7))

plt.title('Algorithm Comparison of Infectious SocioPatterns', size=20)

plt.bar(X, Y, width=0.5, label='DESA', fc='deepskyblue')
plt.bar(X1, Y1, width=0.5, label='SA', fc='lightpink')
plt.bar(X2, Y2, width=0.5, label='TS', fc='darkseagreen')
plt.bar(X3, Y3, width=0.5, label='AGDE', fc='burlywood')
plt.bar(X4, Y4, width=0.5, label='GSK', fc='darkgrey')
plt.legend()
plt.xlabel('Different Algorithm', size=15)
plt.ylabel('Lowest cost of vaccination', size=15)
plt.ylim(70000, 110000)
plt.xlim(-1, 5)
plt.savefig(draw_pathes.revolution_pictures_bar_2)

plt.show()

