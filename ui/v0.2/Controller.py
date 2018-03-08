# -*- coding: utf-8 -*-
# pt5

from View import *

class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super(Controller, self).__init__() #先调用父类的构造函数
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()   # 界面初始设置
        self.connect()  # 绑定信号槽

    def initUi(self):       # 界面初始设置
        # self.setWindowState(Qt::WindowMaximized)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.toolButton_Home_clicked()

    def connect(self):  # 绑定信号槽
        #绑定导航栏按钮
        self.ui.toolButton_Home.clicked.connect(self.toolButton_Home_clicked)
        self.ui.toolButton_FFT.clicked.connect(self.toolButton_FFT_clicked)
        self.ui.toolButton_CWT.clicked.connect(self.toolButton_CWT_clicked)
        self.ui.toolButton_LSTM.clicked.connect(self.toolButton_LSTM_clicked)
        self.ui.toolButton_Set.clicked.connect(self.toolButton_Set_clicked)
        
        #绑定meanBar
        self.ui.opeanFile.triggered.connect(self.menu_opeanFile)
        
    '''  -------------------- ↓ 菜单栏事件 ↓ --------------------  '''
    def menu_opeanFile(self):
        fileName1, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "C:/", "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔  
        print(fileName1,filetype)  



    '''  -------------------- ↓ 导航栏 ↓ --------------------  '''
    # 导航栏更新
    def toolButton_NavigationBar_Update(self,i):
        p = QtGui.QPalette()    
        p.setColor(QtGui.QPalette.Button,QtGui.QColor(44,44,44))

        self.ui.toolButton_Home.setPalette(p)
        self.ui.toolButton_FFT.setPalette(p)
        self.ui.toolButton_CWT.setPalette(p)
        self.ui.toolButton_LSTM.setPalette(p)
        self.ui.toolButton_Set.setPalette(p)

        p.setColor(QtGui.QPalette.Button,QtGui.QColor(128,128,128))   
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



    '''  --------------------↓  ↓ --------------------   '''


