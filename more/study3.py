from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

X1 = np.arange(-4, 4, 0.25)
Y1 = np.arange(-4, 4, 0.25)
# 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
ax.plot_surface(X1, Y1, Z, rstride=1, cstride=1, cmap='rainbow')

plt.show()
