# -*- coding: utf-8 -*-
# PyQt5: pyuic5 -o View.py View.ui
# import sys
from View import *
from Util.Message import Message
from Model.Seg import SegFile,DataTtrack

from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

# 导入matplotlib模块并使用Qt5Agg
import matplotlib
matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

''' ==================== ↓  绘图类   ↓ ==================== '''
class MyFigureCanvasWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyFigureCanvasWidget, self).__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) #设置总的外围边框
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.lineNumber = 0
        self.numberOfRows = 5
        self.leftMargin = 40
        self.topMargin = 5
        self.rightMargin = 5
        self.bottomMargin = 20

    def paint(self, data, lineNumber, numberOfRows):
        # lineNumber 行号,从1开始
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
        self.lineNumber = lineNumber
        self.numberOfRows = numberOfRows
        x = self.leftMargin/self.width()
        y = ( self.height()*(self.numberOfRows - self.lineNumber - 1) /self.numberOfRows + self.bottomMargin )/self.height()
        w = (self.width() - self.leftMargin - self.rightMargin)/self.width()
        h = (self.height()/self.numberOfRows - self.topMargin - self.bottomMargin)/self.height()
        ax = self.figure.add_axes([x, y, w, h])
        ax.plot(data)
        self.canvas.draw()

class MyQPainteWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyQPainteWidget, self).__init__()
        self.data = None
        self.paintX = 0
        self.paintY = 0
        self.paintWidth = 0
        self.paintHeight = 0

    def paintEvent(self,e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectAll(qp)
        self.drawRect(qp)
        qp.end()
        
    def setData(self, data, paintX, paintY, paintWidth, paintHeight):
        self.data = data
        self.paintX = X
        self.paintY = Y
        self.paintWidth = paintWidth
        self.paintHeight = paintHeight
    
    def drawRectAll(self, qp):
        pen = QPen(Qt.black,1,Qt.SolidLine)
        qp.setPen(pen)
        qp.drawRect(10,10, self.width()-10*2, self.height()-10*2)
        
    def drawRect(self, qp):
        pass

class PaintHome(MyQPainteWidget):
    def drawRect(self, qp):
        pass

class PaintFFT(MyQPainteWidget):
    def drawRect(self, qp):
        if self.data != None :
            pass

class PaintCWT(MyQPainteWidget):
    def drawRect(self, qp):
        pass

class PaintLSTM(MyQPainteWidget):
    def drawRect(self, qp):
        pass

class PaintSet(MyQPainteWidget):
    def drawRect(self, qp):
        pass

''' ==================== ↓  控制   ↓ ==================== '''
class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super(Controller, self).__init__()  # 先调用父类的构造函数
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()   # 界面初始设置
        self.connect()  # 绑定信号槽
        self.addPainteWidget() #添加绘图控件

    def initUi(self):       # 界面初始设置
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.toolButton_Home_clicked()
 
    def connect(self):  # 绑定信号槽
        # 绑定导航栏按钮
        self.ui.toolButton_Home.clicked.connect(self.toolButton_Home_clicked)
        self.ui.toolButton_FFT.clicked.connect(self.toolButton_FFT_clicked)
        self.ui.toolButton_CWT.clicked.connect(self.toolButton_CWT_clicked)
        self.ui.toolButton_LSTM.clicked.connect(self.toolButton_LSTM_clicked)
        self.ui.toolButton_Set.clicked.connect(self.toolButton_Set_clicked)

        # 绑定meanBar
        self.ui.opeanFile.triggered.connect(self.menu_opeanFile)

    '''  -------------------- ↓ 菜单栏事件 ↓ --------------------  '''

    def menu_opeanFile(self):
        fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(
            self, "选取文件", "C:/", "seg Files (*.seg)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.segFile = SegFile()
        
        reply = self.segFile.loadFile(fileName)
        if(reply != 0):
            QtWidgets.QMessageBox.warning(
                self, "Warning", Message().dict[reply], QtWidgets.QMessageBox.Yes)
        else:
            pass

        for i in range(0,self.segFile.tapeNum):
            self.paintFFT.paint(self.segFile.dataList[i].data,i,self.segFile.tapeNum)
 
    # 导航栏更新

    def toolButton_NavigationBar_Update(self, i):
        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Button, QtGui.QColor(44, 44, 44))

        self.ui.toolButton_Home.setPalette(p)
        self.ui.toolButton_FFT.setPalette(p)
        self.ui.toolButton_CWT.setPalette(p)
        self.ui.toolButton_LSTM.setPalette(p)
        self.ui.toolButton_Set.setPalette(p)

        p.setColor(QtGui.QPalette.Button, QtGui.QColor(128, 128, 128))
        if i == 0:
            self.ui.toolButton_Home.setPalette(p)
        if i == 1:
            self.ui.toolButton_FFT.setPalette(p)
        if i == 2:
            self.ui.toolButton_CWT.setPalette(p)
        if i == 3:
            self.ui.toolButton_LSTM.setPalette(p)
        if i == 4:
            self.ui.toolButton_Set.setPalette(p)

        self.ui.stackedWidget_Panel.setCurrentIndex(i)
        self.ui.stackedWidget_Canvs.setCurrentIndex(i)

    def toolButton_Home_clicked(self):
        self.toolButton_NavigationBar_Update(0)

    def toolButton_FFT_clicked(self):
        self.toolButton_NavigationBar_Update(1)

    def toolButton_CWT_clicked(self):
        self.toolButton_NavigationBar_Update(2)

    def toolButton_LSTM_clicked(self):
        self.toolButton_NavigationBar_Update(3)

    def toolButton_Set_clicked(self):
        self.toolButton_NavigationBar_Update(4)

    '''  --------------------↓ 添加绘图控件 ↓ --------------------   '''
    def addPainteWidget(self):
        #self.paintFFT  = PaintFFT()
        #self.ui.gridLayout_Canvas_FFT.addWidget(self.paintFFT)
        self.paintFFT = MyFigureCanvasWidget()
        self.ui.gridLayout_Canvas_FFT.addWidget(self.paintFFT)
        
        self.paintCWT = PaintCWT()
        self.ui.gridLayout_Canvas_CWT.addWidget(self.paintCWT)

        self.paintLSTM = PaintLSTM()
        self.ui.gridLayout_Canvas_LSTM.addWidget(self.paintLSTM)






        
        

        


