import numpy as np
import matplotlib.pyplot as plt
import draw_pathes

# y_blank=np.loadtxt(draw_pathes.highland_blank_output)
# y0=np.linspace(y_blank,y_blank,21)
y = np.loadtxt(draw_pathes.highland_rand_to_best_output)
y1 = np.loadtxt(draw_pathes.highland_rand2_output)
y2 = np.loadtxt(draw_pathes.highland_current_to_rand_output)
y3 = np.loadtxt(draw_pathes.highland_no_crossover_output)
y4 = np.loadtxt(draw_pathes.highland_current_to_best_output)
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
plt.title('highland', size=18)
# plt.plot(x, y0, label='blank', linewidth=1, color='black')
plt.plot(x, y, label='rand_to_best', linewidth=1, color='r', marker='o')  # linestyle='dotted'
plt.plot(x, y1, label='rand2', linewidth=1, color='b', marker='*')  # linestyle='dashed'
plt.plot(x, y2, label='current_to_rand', linewidth=1, color='g', marker='^')
plt.plot(x, y4, label='current_to_best', linewidth=1, color='y', marker='x')
plt.plot(x, y3, label='no_crossover', linewidth=1, color='indigo', marker='.')

plt.legend()  # 给label用的
plt.grid(alpha=0.4, linestyle='--')
plt.xlabel('Iteration', size=15)
plt.ylabel('Objective function value', size=15)
plt.xticks([i for i in range(0, 105, 5)])
# plt.xlabel_params(labelsize=23)
ax2=fig.add_subplot(1,2,2)
x1= [i for i in range(20, 105, 5)]
y=y[4:]
y1=y1[4:]
y2=y2[4:]
y3=y3[4:]
y4=y4[4:]
#plt.figure(figsize=(8, 6))
plt.title('highland_subgraph', size=18)
# plt.plot(x, y0, label='blank', linewidth=1, color='black')
plt.plot(x1, y, label='rand_to_best', linewidth=1, color='r', marker='o')  # linestyle='dotted'
plt.plot(x1, y1, label='rand2', linewidth=1, color='b', marker='*')  # linestyle='dashed'
plt.plot(x1, y2, label='current_to_rand', linewidth=1, color='g', marker='^')
plt.plot(x1, y4, label='current_to_best', linewidth=1, color='y', marker='x')
plt.plot(x1, y3, label='no_crossover', linewidth=1, color='indigo', marker='.')

plt.legend()  # 给label用的
plt.grid(alpha=0.4, linestyle='--')
plt.xlabel('Iteration', size=15)
plt.ylabel('Objective function value', size=15)
plt.savefig(r'C:\project\ocp\draw\pictures\highland_1')
plt.show()
