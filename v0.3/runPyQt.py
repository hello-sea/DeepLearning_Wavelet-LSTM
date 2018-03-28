# -*- coding: utf-8 -*-

from View import Ui_MainWindow
from PyQt5 import QtWidgets

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__() #先调用父类的构造函数
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":   
    import sys
    app = QtWidgets.QApplication(sys.argv)   
    myapp = App()
    myapp.show()   
    sys.exit(app.exec_())  
    pass
