# -*- coding: utf-8 -*-

from Controller.Controller import Controller
from PyQt5 import QtWidgets


if __name__ == "__main__":   
    import sys
    app = QtWidgets.QApplication(sys.argv)   
    myapp = Controller()
    myapp.show()   
    sys.exit(app.exec_())  
    pass


