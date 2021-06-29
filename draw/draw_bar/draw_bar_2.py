import numpy as np
import matplotlib.pyplot as plt
import pathes
from draw import draw_pathes

name_list = ['bundesliga', 'highland', 'highschool', 'hiv', 'league']
# 柱高信息
Y = [0, 0, 0, 0, 0]
Y1 = [0, 0, 0, 0, 0]
Y2 = [0, 0, 0, 0, 0]
Y3 = [0, 0, 0, 0, 0]

i=0
with open(pathes.bundesliga_output) as f:
    lines = f.readlines()
j = 2
lines.pop(0)
lines = np.array(lines)
for line in lines:
    numbers = [float(j) for j in line.split()]
Y[i]=numbers[1]
Y1[i]=numbers[2]
npsai=np.loadtxt(pathes.bundesliga_SA_output)
nptsi=np.loadtxt(pathes.bundesliga_TS_output)
Y2[i]=npsai[20]
Y3[i]=nptsi[20]

i=1
with open(pathes.highland_output) as f:
    lines = f.readlines()
j = 2
lines.pop(0)
lines = np.array(lines)
for line in lines:
    numbers = [float(j) for j in line.split()]
Y[i]=numbers[1]
Y1[i]=numbers[2]
npsai=np.loadtxt(pathes.highland_SA_output)
nptsi=np.loadtxt(pathes.highland_TS_output)
Y2[i]=npsai[20]
Y3[i]=nptsi[20]
print(Y2[i])

i=2
with open(pathes.highshcool_output) as f:
    lines = f.readlines()
j = 2
lines.pop(0)
lines = np.array(lines)
for line in lines:
    numbers = [float(j) for j in line.split()]
Y[i]=numbers[1]
Y1[i]=numbers[2]
npsai=np.loadtxt(pathes.highshcool_SA_output)
nptsi=np.loadtxt(pathes.highshcool_TS_output)
Y2[i]=npsai[20]
Y3[i]=nptsi[20]
print(Y2[i])
# for line in lines:
#     numbers = [float(i) for i in line.split()]
#     Y[i] = numbers[1]
#     Y1[i] = numbers[2]
#     i += 1

X = list(range(len(Y)))

total_width, n = 0.6, 2
width = total_width / n

fig=plt.figure(figsize=(9, 7))

plt.title('Algorithm_Comparison_1', size=20)

# plt.ylim(80, int(max(Y2) + 1))
# plt.yticks(range(int(min(Y1)), int(max(Y) + 3), 1))

plt.bar(X, Y, width=width, label='DE', tick_label=name_list, fc='indigo')
for i in range(len(X)):
    X[i] = X[i] + width
plt.bar(X, Y1, width=width, label='DESA', tick_label=name_list, fc='r')
for i in range(len(X)):
    X[i] = X[i] + width
plt.bar(X, Y2, width=width, label='SA', tick_label=name_list, fc='y')
for i in range(len(X)):
    X[i] = X[i] + width
plt.bar(X, Y3, width=width, label='TS', tick_label=name_list, fc='g')
plt.legend()
plt.xlabel('Different Strategy', size=15)
plt.ylabel('Objective function value', size=15)

# plt.savefig(draw_pathes.bundesliga_pictures_bar_2)

plt.show()

