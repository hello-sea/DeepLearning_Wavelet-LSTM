# -*- coding: utf-8 -*-

from Controller import *


if __name__ == "__main__":   
    import sys
    app = QtWidgets.QApplication(sys.argv)   
    myapp = Controller()
    myapp.show()   
    sys.exit(app.exec_())  
    pass
