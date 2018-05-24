# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
# 导入matplotlib模块并使用Qt5Agg
import matplotlib
matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

''' ==================== ↓  绘图类   ↓ ==================== '''
class MyFigureCanvas(QtWidgets.QWidget):
    def __init__(self,figureNumber): 
        super(MyFigureCanvas, self).__init__()
        
        ''' 严重警告: self.figure = plt.figure( 0 ) 0是指定全局标识 '''
        self.figureNumber = figureNumber
        self.figure = plt.figure(self.figureNumber)

        self.canvas = FigureCanvas(self.figure)
        
        self.layout = QtWidgets.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0) #设置总的外围边框
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.axList = []

        self.numberOfRows = 1 #图片个数 (排列行数),默认为 1
        self.leftMargin = 40
        self.topMargin = 5
        self.rightMargin = 5
        self.bottomMargin = 20

    def setAx(self, lineNumber, numberOfRows, MyProjection): 
        # lineNumber: 第几行, numberOfRows: 行数
        # 如 setAx(0,1) 表示 第 1 行, 共 1 行
        ''' 
        def paint(self, data, lineNumber, numberOfRows, leftMargin, topMargin, rightMargin, bottomMargin):
            self.lineNumber = lineNumber
            self.numberOfRows = numberOfRows
            self.leftMargin = leftMargin
            self.topMargin = topMargin
            self.rightMargin = rightMargin
            self.bottomMargin = bottomMargin
        '''
        pass
        ''' ax = self.figure.add_axes([0.05,0.05,0.9,0.9])
            ax = self.figure.add_subplot(5,1,1)     
        '''
        self.numberOfRows = numberOfRows
        self.x = self.leftMargin/self.width()
        self.y = ( self.height()*(self.numberOfRows - (lineNumber + 1 ) ) /self.numberOfRows + self.bottomMargin )/self.height()
        self.w = (self.width() - self.leftMargin - self.rightMargin)/self.width()
        self.h = (self.height()/self.numberOfRows - self.topMargin - self.bottomMargin)/self.height()
        
        if MyProjection == '3d':
            # ax = self.figure.add_axes([self.x, self.y, self.w, self.h],projection='3d')
            ax = self.figure.add_axes([self.x, self.y, self.w, self.h],projection = MyProjection)
            ax.set_ylabel("scale")
            ax.set_xlabel("time")
            # ax.set_title("a straight line (OO)")
        else :
            ax = self.figure.add_axes([self.x, self.y, self.w, self.h])
            # ax.set_xlabel("x value")
            # ax.set_ylabel("y value")
            # ax.set_title("a straight line (OO)")
        
        self.axList.append( ax )        

        
    def paint(self, lineNumber, data):
        # lineNumber: 第几行, data: 绘图数据
        pass
    
    def figureClear(self):
        self.figure.clf()
        self.axList = []

class MyFigureCanvasFFT(MyFigureCanvas):
    def paint(self, lineNumber, data):
        self.axList[lineNumber].clear()
        self.axList[lineNumber].plot(data, 'k') # k 黑色
        self.canvas.draw()

class MyFigureCanvasCWT(MyFigureCanvas):     
    def MyMatshow(self, lineNumber, data): 
        self.axList[lineNumber].clear()
        self.axList[lineNumber].matshow(data)
        self.canvas.draw()

    def My3DView_init(self,lineNumber,MyElev,MyAzim):
        '''     - lineNumber：指定第几幅图
            view_init(elev=MyElev,azim=MyAzim) 
                - elev: 竖直 角度
                - azim: 水平 角度
        '''
        self.axList[lineNumber].view_init(elev=MyElev,azim=MyAzim)

    def MyPlot_surface(self, lineNumber, data, stepX, stepY):
        ''' stepX = 2  # 采样步长 X
            stepY = 10  # 采样步长 Y
        '''
        # ax = self.figure.add_axes([0.05,0.05,0.9,0.9],projection='3d')
        # ax = Axes3D( self.figure )

        X = range(0, len(data), stepX)      #频率
        Y = range(0, len(data[0]), stepY)   #时间

        XX , YY= np.meshgrid(X, Y)  # XX[i]、YY[i]代表时间 ; XX[0][i]、YY[0][i]代表频率
        ZZ = np.zeros([len( Y ), len( X )])  # ZZ[i]代表时间、ZZ[0][i]代表频率

        for i in range(0, len( Y )):
            for j in range(0, len( X )):
                ZZ[i][j] = data[ X[j] ][ Y[i] ]

        # 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
        self.axList[lineNumber].plot_surface(XX, YY, ZZ, rstride=1, cstride=1, cmap='rainbow')
        
        # self.canvas.draw()

class MyFigureCanvasLSTM(MyFigureCanvas):
    def paint(self, lineNumber, data):
        pass
        self.axList[lineNumber].clear()
        self.axList[lineNumber].plot(data, 'k') # k 黑色
        self.canvas.draw()


