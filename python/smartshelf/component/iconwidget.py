from smartshelf.ui.iconwidget import Ui_iconWidget

from PySide2.QtWidgets import QMainWindow, QListWidgetItem, QWidget, QLabel, QMenu
from PySide2.QtCore import QSize, Qt, QPoint
from PySide2.QtGui import QIcon, QPixmap, QImage, QFont


class IconWidget(QWidget):
    def __init__(self, cmdObj, parent=None):
        super(IconWidget, self).__init__(parent=parent)
        self.ui = Ui_iconWidget()
        self.ui.setupUi(self)

        self.cmdObj = cmdObj
        self.size = None

        self.setToolTip(self.cmdObj.getCommandName())
        self.defaultStyleSheet = self.styleSheet()

    def updateCmdObj(self):
        self.setToolTip(self.cmdObj.getCommandName())
        self.setSize(self.size)

    def getCommandObject(self):
        return self.cmdObj

    def setSize(self, size):
        self.size = size
        pixmap = self.cmdObj.getIconPixmap().scaled(self.size, Qt.KeepAspectRatio,
                                                    Qt.SmoothTransformation)

        child = self.layout().takeAt(0)
        if child.widget():
            child.widget().deleteLater()

        imageLabel = QLabel()
        self.layout().addWidget(imageLabel)

        imageLabel.setPixmap(pixmap)
        imageLabel.resize(self.size)

        if self.cmdObj.isVisibleName():

            title = QLabel(imageLabel)
            title.setText(self.cmdObj.getCommandName())

            labelSize = title.sizeHint()
            parentSize = imageLabel.size()
            moveX = 0
            moveY = 0

            title.setStyleSheet("background-color:rgba(0,0,0,0.5);")

            if labelSize.width() < parentSize.width():
                moveX = (parentSize.width() - labelSize.width()) / 2 - 4
                title.setStyleSheet(
                    "background-color:rgba(0,0,0,0.5); padding: 0 2px")

            moveY = parentSize.height() - labelSize.height()

            title.move(moveX, moveY)

    def mousePressEvent(self, event):
        self.setStyleSheet("background-color:transparent")
        super(IconWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet(self.defaultStyleSheet)
        super(IconWidget, self).mouseReleaseEvent(event)

    def dragMoveEvent(self, event):
        self.setStyleSheet("background-color:red")
        super(IconWidget, self).dragMoveEvent(event)
