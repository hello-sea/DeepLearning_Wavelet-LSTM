
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

t = np.linspace(0, 2, 200, endpoint=False)
t1 = np.linspace(2, 4, 200, endpoint=False)
t2 = np.linspace(4, 6, 200, endpoint=False)
# print(t1)
sig  = np.sin(4 *2 * np.pi * t) 
sig = sig.tolist()
sig1 = np.sin(6 *2 * np.pi * t1) 
sig1 = sig1.tolist()
sig2 =  np.sin(10 *2 * np.pi * t2)
sig2 = sig2.tolist()

sig_data = sig + sig1 + sig2
print(type(sig_data))
# plt.plot(sig_data)
# plt.show()





import mlpy.wavelet as wave
x = np.random.sample(512)

scales = wave.autoscales(N=x.shape[0], dt=1, dj=0.25, wf='Morlet', p=2)
X = wave.cwt(x=x, dt=1, scales=scales, wf='Morlet', p=2)

fig = plt.figure(1)
ax1 = plt.subplot(2,1,1)
p1 = ax1.plot(x)
ax1.autoscale_view(tight=True)
ax2 = plt.subplot(2,1,2)
p2 = ax2.imshow(np.abs(X), interpolation='nearest')
plt.show()





'''


widths = np.arange(1, 16)
cwtmatr = signal.cwt(sig_data, signal.ricker, widths)
# plt.imshow(cwtmatr, extent=[-1, 1, 31, 1], cmap='PRGn', aspect='auto',
#             vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
# plt.show()

data = cwtmatr
X = range(0, len(data))      #频率
Y = range(0, len(data[0]))   #时间

XX , YY= np.meshgrid(X, Y)  # XX[i]、YY[i]代表时间 ; XX[0][i]、YY[0][i]代表频率
ZZ = np.zeros([len( Y ), len( X )])  # ZZ[i]代表时间、ZZ[0][i]代表频率

for i in range(0, len( Y )):
    for j in range(0, len( X )):
        ZZ[i][j] = data[ X[j] ][ Y[i] ]

# 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
figure = plt.figure()
ax = figure.add_axes([0.05,0.05,0.9,0.9], projection = '3d')
ax.plot_surface(XX, YY, ZZ, rstride=1, cstride=1, cmap='rainbow')
plt.show()

'''