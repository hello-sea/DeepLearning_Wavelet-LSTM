# encoding: utf-8 
import pywt
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)

#x = np.arange(512)
#y = np.sin(2*np.pi*x/32)
##txt文件和当前脚本在同一目录下，所以不用写具体路径
filename = 'data.txt' 
data = []
with open(filename, 'r') as file_to_read:
    while True:
        lines = file_to_read.readline() # 整行读取数据
        if not lines:
            break
            pass
        # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
        p_tmp = lines.split() 
        data.append(p_tmp[0])  # 添加新读取的数据
        pass
#print(data)

##plt.subplot(211)
x = np.arange(len(data))
y = data;
#plt.plot(data)
##plt.subplot(212)

coef,freqs=pywt.cwt(y,np.arange(1,128),'gaus1')

#--时频(尺度)度--
plt.matshow( coef ) 

#--频率图(全部叠加)
#plt.plot(freqs)
#l = [i*1000 for i in freqs]
#print(l)
#plt.plot( l )

#--时频度(三维)--
#print(len(coef))
#print(len(coef[0]))
#coef = list(zip(*coef))  

#   x1 = np.arange(len(coef)+1)
#   y1 = np.arange(len(coef[0])+1)

#print(x1)
#print(y1)
#ax.plot_surface( y1 , x1 , coef, rstride=1, cstride=1, cmap='rainbow')
#ax.set_xlabel('t label', color='r')  
#ax.set_ylabel('f label', color='g')  
#ax.set_zlabel('h label', color='b')#给三个坐标轴注明


#coef_T = list(zip(*coef))        
#x1 = np.arange(len(coef_T))
#y1 = np.arange(len(coef_T[0]))
#ax.plot_surface( x1, y1, coef_T, rstride=1, cstride=1, cmap='rainbow')

        
plt.show()




