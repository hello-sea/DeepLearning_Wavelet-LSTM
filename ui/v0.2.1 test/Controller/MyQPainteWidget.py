# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui ,QtCore
# from PyQt5.QtGui import QPainter, QColor, QPen
# from PyQt5.QtCore import Qt

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
        self.paintX = paintX
        self.paintY = paintY
        self.paintWidth = paintWidth
        self.paintHeight = paintHeight
    
    def drawRectAll(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black,1,QtCore.Qt.SolidLine)
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