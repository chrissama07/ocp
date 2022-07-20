import numpy as np
import matplotlib.pyplot as plt
import draw_pathes
from brokenaxes import brokenaxes


y = np.loadtxt(draw_pathes.jazz_rand_to_best_output)
y1 = np.loadtxt(draw_pathes.jazz_rand2_output)
y2 = np.loadtxt(draw_pathes.jazz_current_to_rand_output)
y3 = np.loadtxt(draw_pathes.jazz_no_crossover_output)
y4 = np.loadtxt(draw_pathes.jazz_current_to_best_output)
y5 = np.loadtxt(draw_pathes.jazz_mms_output)
y6 = np.loadtxt(draw_pathes.jazz_immsade_output)
y7 = np.loadtxt(draw_pathes.jazz_agde_output)

fig=plt.figure(figsize=(15, 6))
x = [i for i in range(0, 105, 5)]
ax1=fig.add_subplot(1,2,1)
plt.title('Interaction', size=18)
plt.plot(x, y, label='rand_to_best', linewidth=1, color='r', marker='o')  # linestyle='dotted'
plt.plot(x, y1, label='rand2', linewidth=1, color='b', marker='*')  # linestyle='dashed'
plt.plot(x, y2, label='current_to_rand', linewidth=1, color='g', marker='^')
plt.plot(x, y4, label='current_to_best', linewidth=1, color='y', marker='x')
plt.plot(x, y3, label='no_crossover', linewidth=1, color='indigo', marker='.')
plt.plot(x, y5, label='mms', linewidth=1, color='tan', marker='H')
plt.plot(x, y6, label='immsade', linewidth=1, color='crimson', marker='+')
plt.plot(x, y7, label='agde-mutation', linewidth=1, color='dimgray', marker='<')

plt.legend(loc='lower right', bbox_to_anchor=(1, 0.1))  # 给label用的
plt.grid(alpha=0.4, linestyle='--')
plt.xlabel('Iteration', size=15)
plt.ylabel('Lowest cost of vaccination', size=15)
plt.xticks([i for i in range(0, 105, 5)])
#
ax2=fig.add_subplot(2,2,2)
x1= [i for i in range(5, 50, 5)]
y=y[1:10]
y1=y1[1:10]
y2=y2[1:10]
y3=y3[1:10]
y4=y4[1:10]
y5=y5[1:10]
y6=y6[1:10]
y7=y7[1:10]
plt.title('Interaction Subgraph', size=18)
plt.plot(x1, y, label='rand_to_best', linewidth=1, color='r', marker='o')  # linestyle='dotted'
plt.plot(x1, y1, label='rand2', linewidth=1, color='b', marker='*')  # linestyle='dashed'
plt.plot(x1, y2, label='current_to_rand', linewidth=1, color='g', marker='^')
plt.plot(x1, y4, label='current_to_best', linewidth=1, color='y', marker='x')
plt.plot(x1, y3, label='no_crossover', linewidth=1, color='indigo', marker='.')
plt.plot(x1, y5, label='mms', linewidth=1, color='tan', marker='H')
plt.plot(x1, y6, label='immsade', linewidth=1, color='crimson', marker='+')
plt.plot(x1, y7, label='agde-mutation', linewidth=1, color='dimgray', marker='<')
plt.xticks([i for i in range(5, 50, 5)])
# plt.legend()  # 给label用的
plt.grid(alpha=0.4, linestyle='--')
# plt.xlabel('Iteration', size=15)
# plt.ylabel('Lowest cost of vaccination', size=15)

# plt.xticks([i for i in range(0, 50, 5)])
# bax = brokenaxes(ylims=((225, 235), (260, 265)), despine=False)
# ax3=fig.add_subplot(1,2,2)
# x2= [i for i in range(5, 50, 5)]
#
# plt.title('Hiv Subgraph 2', size=18)
#
# plt.plot(x2, y5, label='mms', linewidth=1, color='tan', marker='H')
# plt.plot(x2, y6, label='immsade', linewidth=1, color='crimson', marker='+')
# plt.plot(x2, y5, label='agde-mutation', linewidth=1, color='dimgray', marker='<')
#
# # plt.xticks([i for i in range(5, 50, 5)])
# plt.legend()  # 给label用的
# plt.grid(alpha=0.4, linestyle='--')
# plt.xlabel('Iteration', size=15)
# plt.ylabel('Lowest cost of vaccination', size=15)
# plt.xticks([])

ax3 = fig.add_subplot(2,2,4)

# plt.title('Highschool Subgraph 1', size=18)
plt.plot(x1, y, label='rand_to_best', linewidth=1, color='r', marker='o')  # linestyle='dotted'
plt.plot(x1, y1, label='rand2', linewidth=1, color='b', marker='*')  # linestyle='dashed'
plt.plot(x1, y2, label='current_to_rand', linewidth=1, color='g', marker='^')
plt.plot(x1, y4, label='current_to_best', linewidth=1, color='y', marker='x')
plt.plot(x1, y3, label='no_crossover', linewidth=1, color='indigo', marker='.')
plt.plot(x1, y5, label='mms', linewidth=1, color='tan', marker='H')
plt.plot(x1, y6, label='immsade', linewidth=1, color='crimson', marker='+')
plt.plot(x1, y7, label='agde-mutation', linewidth=1, color='dimgray', marker='<')
plt.xticks([i for i in range(5, 50, 5)])
# plt.legend()  # 给label用的
plt.grid(alpha=0.4, linestyle='--')
plt.xlabel('Iteration', size=15)
# plt.ylabel('Lowest cost of vaccination', size=15)
ax3.set_ylabel('Lowest cost of vaccination', size=15)
ax3.yaxis.set_label_coords(-0.1, 1)

plt.xticks([i for i in range(0, 50, 5)])
ax2.set_ylim(1313.3, 1314.8)
ax3.set_ylim(1085, 1122)
ax2.spines['bottom'].set_visible(False)
ax3.spines['top'].set_visible(False)
ax2.xaxis.tick_top()
ax2.tick_params(labeltop='off')
ax3.xaxis.tick_bottom()
d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
ax2.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax2.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
kwargs.update(transform=ax3.transAxes)  # switch to the bottom axes
ax3.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax3.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

plt.savefig(draw_pathes.jazz_pictures_linechart_1)
plt.show()