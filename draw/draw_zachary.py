import numpy as np
import matplotlib.pyplot as plt
import draw_pathes


y = np.loadtxt(draw_pathes.zachary_rand_to_best_output)
y1 = np.loadtxt(draw_pathes.zachary_rand2_output)
y2 = np.loadtxt(draw_pathes.zachary_current_to_rand_output)
y3 = np.loadtxt(draw_pathes.zachary_no_crossover_output)
y4 = np.loadtxt(draw_pathes.zachary_current_to_best_output)

fig=plt.figure(figsize=(15,6))
x = [i for i in range(0, 105, 5)]
ax1=fig.add_subplot(1,2,1)
plt.title('zachary', size=18)
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
ax2=fig.add_subplot(1,2,2)
x1= [i for i in range(5, 50, 5)]
y=y[1:10]
y1=y1[1:10]
y2=y2[1:10]
y3=y3[1:10]
y4=y4[1:10]
plt.title('zachary_subgraph', size=18)
plt.plot(x1, y, label='rand_to_best', linewidth=1, color='r', marker='o')  # linestyle='dotted'
plt.plot(x1, y1, label='rand2', linewidth=1, color='b', marker='*')  # linestyle='dashed'
plt.plot(x1, y2, label='current_to_rand', linewidth=1, color='g', marker='^')
plt.plot(x1, y4, label='current_to_best', linewidth=1, color='y', marker='x')
plt.plot(x1, y3, label='no_crossover', linewidth=1, color='indigo', marker='.')
plt.xticks([i for i in range(5, 50, 5)])
plt.legend()  # 给label用的
plt.grid(alpha=0.4, linestyle='--')
plt.xlabel('Iteration', size=15)
plt.ylabel('Objective function value', size=15)
plt.savefig(draw_pathes.zachary_pictures_linechart_1)
plt.show()
