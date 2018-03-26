from PyQt5.QtCore import (pyqtProperty, pyqtSignal, QEasingCurve, QObject,
        QParallelAnimationGroup, QPointF, QPropertyAnimation, qrand, QRectF,
        QState, QStateMachine, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QLinearGradient, QPainter, QPainterPath,
        QPixmap)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
        QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsWidget,
        QStyle)

# import animatedtiles_rc


# PyQt doesn't support deriving from more than one wrapped class so we use
# composition and delegate the property.
class Pixmap(QObject):
    def __init__(self, pix):
        #父类初始化
        super(Pixmap, self).__init__()

        self.pixmap_item = QGraphicsPixmapItem(pix)
        self.pixmap_item.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    # 类似于C# 字段调用方法  python里面property函数
    pos = pyqtProperty(QPointF, fset=_set_pos)


class Button(QGraphicsWidget):
    pressed = pyqtSignal()

    def __init__(self, pixmap, parent_arg=None):
        #QGraphicsWidget ：_init__ (self, QGraphicsItem parent = None, Qt.WindowFlags wFlags = 0)
        #The QGraphicsWidget class is the base class for all widget items in a QGraphicsScene
        super(Button, self).__init__(parent_arg)

        self._pix = pixmap
        #设置悬停时间是否接受，系统一直跟随鼠标检测是否悬停在一个控件上
        self.setAcceptHoverEvents(True)
        #设置缓存的模式 加速图形的渲染 这个选项是在绘图层起作用 适用于平移运动的图形，不适用于旋转伸缩变换
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        

    #限制绘图的边界 所有的绘图都必须在这个区域的内部，这个区域是矩形的
    def boundingRect(self):
        #将控件的坐标原点设置成了控件的中心
        return QRectF(-65, -65, 130, 130)

    #图形的边界必须是矩形，图形的形状可以是任意图形
    def shape(self):
        #QPainterPath为绘图操作提供了一个容器，为图形形状的构造和重用提供了一种方式
        # 初始化方法
        #addEllipse (self, QRectF rect)
        #addEllipse (self, float x, float y, float w, float h)
        #addEllipse (self, QPointF center, float rx, float ry)

        path = QPainterPath()
        path.addEllipse(self.boundingRect())

        return path

    def paint(self, painter, option, widget):
        #检查是否处于按下的状态
        down = option.state & QStyle.State_Sunken
        r = self.boundingRect()

        grad = QLinearGradient(r.topLeft(), r.bottomRight())
        #这段代码是检查鼠标是否在控件上如果是那么修改亮度渐变的梯度
        if option.state & QStyle.State_MouseOver:
            color_0 = Qt.white
        else:
            color_0 = Qt.lightGray
        color_1 = Qt.darkGray

        if down:
            color_0, color_1 = color_1, color_0

        grad.setColorAt(0, color_0)
        grad.setColorAt(1, color_1)

        painter.setPen(Qt.darkGray)
        painter.setBrush(grad)
        painter.drawEllipse(r)

        color_0 = Qt.darkGray
        color_1 = Qt.lightGray

        if down:
            color_0, color_1 = color_1, color_0

        grad.setColorAt(0, color_0)
        grad.setColorAt(1, color_1)

        painter.setPen(Qt.NoPen)
        painter.setBrush(grad)

        if down:
            #painter.translate(2,2) 是将原点设置为（2,2）
            painter.translate(2, 2)
        # r.adjust对原来的矩形的大小进行调整 获得新的矩形大小
        painter.drawEllipse(r.adjusted(5, 5, -5, -5))
        painter.drawPixmap(-self._pix.width() / 2, -self._pix.height() / 2,self._pix)


    def mousePressEvent(self, ev):
        #出发鼠标按下的事件
        self.pressed.emit()
        self.update()

    def mouseReleaseEvent(self, ev):
        self.update()


class View(QGraphicsView):
    def resizeEvent(self, event):
        #调用父类的事件
        super(View, self).resizeEvent(event)
        #尽量填充该矩形同时保持图片应有的比例
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def mouseMoveEvent(self,event):
        self.setWindowTitle(f'{event.x()},{event.y()}')
        self.update()

if __name__ == '__main__':

    import sys
    import math

    app = QApplication(sys.argv)

    kineticPix = QPixmap(':/images/kinetic.png')
    bgPix = QPixmap(':/images/Time-For-Lunch-2.jpg')
    #param  x,y,width,height
    scene = QGraphicsScene(-350, -350, 700, 700)

    items = []
    for i in range(64):
        item = Pixmap(kineticPix)
        item.pixmap_item.setOffset(-kineticPix.width() / 2,
                -kineticPix.height() / 2)
        #setZvalue是设置图层的叠加顺序，数字大的叠加在数字小的上方
        item.pixmap_item.setZValue(i)
        items.append(item)
        scene.addItem(item.pixmap_item)

    # Buttons.
    #The QGraphicsRectItem class provides a rectangle item that you can add to a QGraphicsScene
    buttonParent = QGraphicsRectItem()
    #buttonparent作为Buttons的父类的初始化参数
    ellipseButton = Button(QPixmap(':/images/ellipse.png'), buttonParent)
    figure8Button = Button(QPixmap(':/images/figure8.png'), buttonParent)
    randomButton = Button(QPixmap(':/images/random.png'), buttonParent)
    tiledButton = Button(QPixmap(':/images/tile.png'), buttonParent)
    centeredButton = Button(QPixmap(':/images/centered.png'), buttonParent)

    ellipseButton.setPos(-100, -100)
    figure8Button.setPos(100, -100)
    randomButton.setPos(0, 0)
    tiledButton.setPos(-100, 100)
    centeredButton.setPos(100, 100)

    scene.addItem(buttonParent)
    buttonParent.setScale(0.75)
    buttonParent.setPos(200, 200)
    buttonParent.setZValue(65)

    # States.
    rootState = QState()
    ellipseState = QState(rootState)
    figure8State = QState(rootState)
    randomState = QState(rootState)
    tiledState = QState(rootState)
    centeredState = QState(rootState)

    # Values.
    for i, item in enumerate(items):
        # Ellipse.
        ellipseState.assignProperty(item, 'pos',
                QPointF(math.cos((i / 63.0) * 6.28) * 250,
                        math.sin((i / 63.0) * 6.28) * 250))

        # Figure 8.
        figure8State.assignProperty(item, 'pos',
                QPointF(math.sin((i / 63.0) * 6.28) * 250,
                        math.sin(((i * 2)/63.0) * 6.28) * 250))

        # Random.
        #qrand()返回0-randMax之间的数值 qrand()%500 将随机数限制在0-499
        randomState.assignProperty(item, 'pos',
                QPointF(-250 + qrand() % 500, -250 + qrand() % 500))

        # Tiled.
        tiledState.assignProperty(item, 'pos',
                QPointF(((i % 8) - 4) * kineticPix.width() + kineticPix.width() / 2,
                        ((i // 8) - 4) * kineticPix.height() + kineticPix.height() / 2))

        # Centered.
        centeredState.assignProperty(item, 'pos', QPointF())

    # Ui.
    view = View(scene)
    view.setWindowTitle("Animated Tiles")
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    view.setBackgroundBrush(QBrush(bgPix))
    view.setCacheMode(QGraphicsView.CacheBackground)
    view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
    view.show()


    #状态机
    states = QStateMachine()
    states.addState(rootState)
    states.setInitialState(rootState)
    rootState.setInitialState(centeredState)

    group = QParallelAnimationGroup()
    for i, item in enumerate(items):
        anim = QPropertyAnimation(item, b'pos')
        anim.setDuration(750 + i * 25*1)
        #设置用于动画的擦除效果 每张图片的运动轨迹
        # doc http://doc.qt.io/qt-4.8/qeasingcurve.html
        anim.setEasingCurve(QEasingCurve.InOutBack)
        group.addAnimation(anim)

    trans = rootState.addTransition(ellipseButton.pressed, ellipseState)
    trans.addAnimation(group)

    trans = rootState.addTransition(figure8Button.pressed, figure8State)
    trans.addAnimation(group)

    trans = rootState.addTransition(randomButton.pressed, randomState)
    trans.addAnimation(group)

    trans = rootState.addTransition(tiledButton.pressed, tiledState)
    trans.addAnimation(group)

    trans = rootState.addTransition(centeredButton.pressed, centeredState)
    trans.addAnimation(group)

    timer = QTimer()
    timer.start(125)
    timer.setSingleShot(True)
    trans = rootState.addTransition(timer.timeout, ellipseState)
    trans.addAnimation(group)

    states.start()

    sys.exit(app.exec_())