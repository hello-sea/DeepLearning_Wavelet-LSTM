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

    def setAx(self, lineNumber, numberOfRows): 
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
        
        self.axList.append( self.figure.add_axes([self.x, self.y, self.w, self.h]) )        
        # self.axList[lineNumber]set_title("a straight line (OO)")
        # self.axList[lineNumber]set_xlabel("x value")
        # self.axList[lineNumber]set_ylabel("y value")
        
    def paint(self, lineNumber, data):
        # lineNumber: 第几行, data: 绘图数据
        pass
    
    def figureClear(self):
        self.figure.clf()
        self.axList = []

class MyFigureCanvasFFT(MyFigureCanvas):
    # def __init__(self,figureNumber): 
    #     super(MyFigureCanvasFFT, self).__init__(figureNumber)

    def paint(self, lineNumber, data):
        # lineNumber: 第几行, data: 绘图数据
        self.axList[lineNumber].clear()
        self.axList[lineNumber].plot(data)
        self.canvas.draw()
    
class MyFigureCanvasCWT(MyFigureCanvas):
    # def __init__(self,figureNumber): 
    #     super(MyFigureCanvasCWT, self).__init__(figureNumber)
    
    def paint(self, lineNumber, data):
        # lineNumber: 第几行, data: 绘图数据
        # figure(self.figureNumber)
        self.axList[lineNumber].clear()
        self.axList[lineNumber].matshow(data)
        self.canvas.draw()

class MyFigureCanvasLSTM(MyFigureCanvas):
    # def __init__(self,figureNumber): 
    #     super(MyFigureCanvasLSTM, self).__init__(figureNumber)
    def paint(self, lineNumber, data):
        # lineNumber: 第几行, data: 绘图数据
        pass
