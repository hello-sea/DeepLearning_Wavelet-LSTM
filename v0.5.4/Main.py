# -*- coding: utf-8 -*-

from MyController.Controller import Controller
from PyQt5 import QtWidgets

# PyQt5: pyuic5 -o View.py View.ui


if __name__ == "__main__":   
    import sys
    app = QtWidgets.QApplication(sys.argv)   
    myapp = Controller()
    myapp.show()   
    sys.exit(app.exec_())  
    pass
	
	
	
'''  runPyQt.py '''
'''
# -*- coding: utf-8 -*-

from View import Ui_MainWindow
from PyQt5 import QtWidgets,QtCore

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__() #先调用父类的构造函数
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setWindowState(QtCore.Qt.WindowMaximized) 

if __name__ == "__main__":   
    import sys
    app = QtWidgets.QApplication(sys.argv)   
    myapp = App()
    myapp.show()   
    sys.exit(app.exec_())  
    pass

'''


