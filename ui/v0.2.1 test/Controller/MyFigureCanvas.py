# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


''' ***** 绘图包 ***** '''
# 导入matplotlib模块并使用Qt5Agg
import matplotlib
matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


''' ==================== ↓  绘图类   ↓ ==================== '''
class MyFigureCanvas(QtWidgets.QWidget):

    ''' 严重警告: 动态添加控件时,要指定<父容器> '''
    def __init__(self,UpWidget): 
        super(MyFigureCanvas, self).__init__(UpWidget)
        self.figure = plt.figure(0)
        self.canvas = FigureCanvas(self.figure)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0) #设置总的外围边框
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.axList = []

        # self.lineNumber = 0
        self.numberOfRows = 1 #图片个数 (排列行数)
        self.leftMargin = 40
        self.topMargin = 5
        self.rightMargin = 5
        self.bottomMargin = 20

        self.iheight = self.height()
        self.iwidth = self.width()

    def setAx(self, lineNumber, numberOfRows): 
        # lineNumber: 第几行, numberOfRows: 行数
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
        # self.numberOfRows = numberOfRows
        # self.x = self.leftMargin/self.width()
        # self.y = ( self.height()*(self.numberOfRows - (lineNumber + 1 ) ) /self.numberOfRows + self.bottomMargin )/self.height()
        # self.w = (self.width() - self.leftMargin - self.rightMargin)/self.width()
        # self.h = (self.height()/self.numberOfRows - self.topMargin - self.bottomMargin)/self.height()
        
        # ax = self.figure.add_axes([x, y, w, h])
        # ax.set_title("a straight line (OO)")
        # ax.set_xlabel("x value")
        # ax.set_ylabel("y value")
        # self.axList.append( self.figure.add_axes([self.x, self.y, self.w, self.h]) )
        self.axList.append( self.figure.add_axes([0.05, 0.05, 0.9, 0.9]) )

    def paint(self, data, lineNumber):
        # data: 绘图数据, lineNumber: 第几行
        self.axList[lineNumber].clear()
        self.axList[lineNumber].plot(data)
        self.canvas.draw()


class MyFigureCanvasFFT(MyFigureCanvas):
    def __init__(self,UpWidget):
        super(MyFigureCanvasFFT, self).__init__(UpWidget)

