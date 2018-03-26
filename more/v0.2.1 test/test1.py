import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
 
 
 
class Example(QtWidgets.QWidget):
 
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
         
    def initUI(self): 
 
        self.setWindowTitle( "Test" )
        self.setGeometry(500, 500, 300, 300)
 
    def paintEvent(self, e):
 
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRect(qp)            
        qp.end()
                             
    def drawRect(self, qp):
         
        qp.setBrush(QtGui.QColor(0, 0, 0, 255))
        qp.drawRect(50, 50, 50, 50)
         
             
if __name__ == '__main__':
     
    app = QtWidgets.QApplication(sys.argv)
    hi = Example()
    hi.show()
    app.exec_()