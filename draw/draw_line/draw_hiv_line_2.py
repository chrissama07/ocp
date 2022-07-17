import numpy as np
import matplotlib.pyplot as plt
from draw import draw_pathes
import pathes

# y_blank=np.loadtxt(draw_pathes.hiv_blank_output)
# y0=np.linspace(y_blank,y_blank,21)
y = np.loadtxt(draw_pathes.hiv_rand_to_best_output)
y1 = np.loadtxt(draw_pathes.hiv_rand2_output)
y2 = np.loadtxt(draw_pathes.hiv_current_to_rand_output)
y3 = np.loadtxt(draw_pathes.hiv_no_crossover_output)
y4 = np.loadtxt(draw_pathes.hiv_current_to_best_output)
y5 = np.loadtxt(pathes.hiv_TS_output)
y6 = np.loadtxt(pathes.hiv_SA_output)
y7 = np.loadtxt(draw_pathes.hiv_mms_output)
y8 = np.loadtxt(draw_pathes.hiv_immsade_output)
y9 = np.loadtxt(draw_pathes.hiv_agde_output)
y10 = np.loadtxt(pathes.hiv_agde_algorithm)
y11 = np.loadtxt(pathes.hiv_GSK)
# for i in range(20):
#     with open(str[i], 'r') as f:
#         content = f.read()
#         y.append(eval(content))  # 将str变成list
#         print('i', i, y[i], type(y[i]))
# x=[10,20,30,40,50,60]
# y=[29,3,45,76,23,89]
#
# x1=[15,25,35,45,55,65]
# y1=[9,7,55,66,33,99]
fig=plt.figure(figsize=(15,6))
x = [i for i in range(0, 105, 5)]
ax1=fig.add_subplot(1,2,1)
#plt.figure(figsize=(8, 6))
plt.title('Hiv', size=18)
# plt.plot(x, y0, label='blank', linewidth=1, color='black')
# plt.plot(x, y, label='rand_to_best', linewidth=1, color='r', marker='o')  # linestyle='dotted'
# plt.plot(x, y1, label='rand2', linewidth=1, color='b', marker='*')  # linestyle='dashed'
# plt.plot(x, y2, label='current_to_rand', linewidth=1, color='g', marker='^')
# plt.plot(x, y4, label='current_to_best', linewidth=1, color='g', marker='^')
# plt.plot(x, y3, label='no_crossover', linewidth=1, color='indigo', marker='.')
plt.plot(x, y5, label='TS', linewidth=1, color='indigo', marker='.')
plt.plot(x, y6, label='SA', linewidth=1, color= 'y', marker='x')
plt.plot(x, y8, label='immsade', linewidth=1, color='crimson', marker='+')
plt.plot(x, y9, label='agde-mutation', linewidth=1, color='dimgray', marker='<')
plt.plot(x, y7, label='mms', linewidth=1, color='tan', marker='H')
plt.plot(x, y10, label='AGDE', linewidth=1, color='darkgreen', marker='1')
plt.plot(x, y11, label='GSK', linewidth=1, color='deepskyblue', marker='2')

plt.legend()  # 给label用的
plt.grid(alpha=0.4, linestyle='--')
plt.xlabel('Iteration', size=15)
plt.ylabel('Lowest Cost of Vaccination', size=15)
plt.xticks([i for i in range(0, 105, 10)])
# plt.xlabel_params(labelsize=23)
ax2=fig.add_subplot(1,2,2)
x1= [i for i in range(0, 30, 5)]
# y=y[2:12]
y1=y1[0:10]
y4=y4[0:10]
y5=y5[0:10]
y6=y6[0:10]
y7=y7[0:6]
y8=y8[0:6]
y9=y9[0:10]
y10=y10[0:6]
y11=y11[0:6]

plt.xticks([i for i in range(0, 30, 5)])
#plt.figure(figsize=(8, 6))
plt.title('Hiv Subgraph', size=18)
# plt.plot(x, y0, label='blank', linewidth=1, color='black')
# plt.plot(x1, y1, label='rand2', linewidth=1, color='b', marker='*')  # linestyle='dashed'
# plt.plot(x, y2, label='current_to_rand', linewidth=1, color='g', marker='^')
# plt.plot(x1, y4, label='current_to_best', linewidth=1, color='g', marker='^')
# plt.plot(x, y3, label='no_crossover', linewidth=1, color='indigo', marker='.')
# plt.plot(x1, y5, label='TS', linewidth=1, color='indigo', marker='.')
# plt.plot(x1, y6, label='SA', linewidth=1, color= 'y', marker='x')
plt.plot(x1, y8, label='immsade', linewidth=1, color='crimson', marker='+')
# plt.plot(x1, y9, label='agde-mutation', linewidth=1, color='dimgray', marker='<')
plt.plot(x1, y7, label='mms', linewidth=1, color='tan', marker='H')
plt.plot(x1, y10, label='AGDE', linewidth=1, color='darkgreen', marker='1')
plt.plot(x1, y11, label='GSK', linewidth=1, color='deepskyblue', marker='2')

plt.legend()  # 给label用的
plt.grid(alpha=0.4, linestyle='--')
plt.xlabel('Iteration', size=15)
plt.ylabel('Lowest Cost of Vaccination', size=15)
plt.savefig(draw_pathes.hiv_pictures_linechart_2)
plt.show()
