# -*- coding: utf-8 -*-
# PyQt5: pyuic5 -o View.py View.ui

from View import *
from Util.Message import Message
from Model.Seg import Seg

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import sys



class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super(Controller, self).__init__()  # 先调用父类的构造函数
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()   # 界面初始设置
        self.connect()  # 绑定信号槽

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
        self.seg = Seg()

        reply = self.seg.loadFile(fileName)
        if(reply != 0):
            QtWidgets.QMessageBox.warning(
                self, "Warning", Message().dict[reply], QtWidgets.QMessageBox.Yes)
        else:
            pass

 
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
        self.FigureCanvasFFT()
        

    def toolButton_CWT_clicked(self):
        self.toolButton_NavigationBar_Update(2)

    def toolButton_LSTM_clicked(self):
        self.toolButton_NavigationBar_Update(3)

    def toolButton_Set_clicked(self):
        self.toolButton_NavigationBar_Update(4)



    '''  --------------------↓ 绘图 ↓ --------------------   '''
    def FigureCanvasFFT(self):
        pass

        # 清屏

        # 获取绘图并绘制
        fig = plt.figure()
        cavans = FigureCanvas(fig)
        
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.plot([1,2,3,4,5])
        canvas.draw()


        # 将绘制好的图像设置为中心 Widget
        # self.ui.widget_Canvas_FFT.setCentralWidget(cavans)
        #self.ui.setCentralWidget(cavans)

        # self.graphicview = QtWidgets.QGraphicsView(self.ui.gridLayout_Canvas_FFT)  # 第一步，创建一个QGraphicsView，注意同样以gridLayoutWidget为参
        
        # graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        # graphicscene.addWidget(cavans)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        # self.graphicview.setScene(graphicscene) # 第五步，把QGraphicsScene放入QGraphicsView
        # self.graphicview.show()  # 最后，调用show方法呈现图形！Voila!!


        #self.ui.gridLayout_Canvas_FFT.addWidget(self.cavans)
        # self.ui.toolButton = QtWidgets.QToolButton(self.ui.page_Canvas_FFT)
        # self.ui.toolButton.setObjectName("toolButton")
        # self.ui.gridLayout_Canvas_FFT.addWidget(self.ui.toolButton, 0, 0, 1, 1)
        # self.ui.gridLayout_Canvas_FFT.addWidget(self.cavans, 0, 0, 1, 1)






