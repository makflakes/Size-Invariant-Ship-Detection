# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)
        # 'Load image' button
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)
        # Button to change from drag/pan to getting pixel info
        self.btnPixInfo = QtWidgets.QToolButton(self)
        self.btnPixInfo.setText('Enter pixel info mode')
        self.btnPixInfo.clicked.connect(self.pixInfo)
        # self.btnPixInfo2 = QtWidgets.QToolButton(self)
        # self.btnPixInfo2.setText('Land sea mask')
        # self.btnPixInfo2.clicked.connect(self.pixInfo2)
        self.editPixInfo = QtWidgets.QLineEdit(self)
        self.editPixInfo.setReadOnly(True)
        self.viewer.photoClicked.connect(self.photoClicked)
        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)
        HBlayout.addWidget(self.btnPixInfo)
        # HBlayout.addWidget(self.btnPixInfo2)
        HBlayout.addWidget(self.editPixInfo)
        VBlayout.addLayout(HBlayout)

    def loadImage(self,flag):
        self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image', '/home', 'Image files (*.png *.jpg *.jpeg)')
        print(self.fname[0])
        self.viewer.setPhoto(QtGui.QPixmap(self.fname[0]))

    def pixInfo2(self):
        lolFile = str("C:\\Users\\Qurram\\Prog\\sih\\gui\\Final\\LandSeaMask.png")
        self.viewer.setPhoto(QtGui.QPixmap(lolFile))
    def pixInfo(self):
        self.viewer.toggleDragMode()

    def photoClicked(self, pos):
        if self.viewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))

# ---------------------------------------------------------------------------- #
#                                Main app class                                #
# ---------------------------------------------------------------------------- #
class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()


# -------------------------------- UI------------------------------ #

    def initUi(self):
        self.window = Window()
        ##Menu Bar
        #Menu items
        exitAct = QtWidgets.QAction(QtGui.QIcon('exit24.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QtWidgets.qApp.quit)

        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAct)


        ##Toolbar
        exitAct1 = QtWidgets.QAction(QtGui.QIcon('sea.png'), 'Exit', self)
        exitAct1.setShortcut('Ctrl+Q')
        exitAct1.triggered.connect(self.window.pixInfo2)
        
        self.toolbar = self.addToolBar('Land Sea Mask')
        self.toolbar.addAction(exitAct1)
 

        ##Status Bar
        self.statusBar().showMessage('Ready')


        ##Layout
        wid = QtWidgets.QWidget(self)


        #Output widget
        


        
        
        
        
        #Input preview
        self.inputScreen = QtWidgets.QWidget(wid)
        self.previewLabel = QtWidgets.QLabel(self.inputScreen)
        
        box1 = QtWidgets.QVBoxLayout()
        box1.addWidget(self.previewLabel)
        self.inputScreen.setLayout(box1)

        #Status
        statusBox = QtWidgets.QWidget(wid)
        statusText = QtWidgets.QTextEdit(statusBox)
        box3 = QtWidgets.QVBoxLayout()
        box3.addWidget(statusText)
        statusBox.setLayout(box3)

        #Main central widget
        self.setCentralWidget(wid)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.window,0,0,3,1)
        grid.setColumnStretch(0,3)
        grid.addWidget(self.inputScreen,0,1)
        grid.addWidget(statusBox,2,1)
        grid.setColumnStretch(1,1)
        grid.setRowStretch(1,1)

        wid.setLayout(grid)
        
        ##Show UI
        self.setGeometry(300,300, 1200,700)
        self.center()
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('ship.png'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

# ---------------------------------- Events ---------------------------------- #

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure you want to quit?", 
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    
# # ---------------------------------------------------------------------------- #
# #                                    Render                                    #
# # ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = Application()
    sys.exit(app.exec())

