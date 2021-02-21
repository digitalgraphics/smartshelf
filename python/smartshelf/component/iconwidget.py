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

        self.setToolTip(self.cmdObj.getCommandName())
        self.defaultStyleSheet = self.styleSheet()

    def getCommandObject(self):
        return self.cmdObj

    def setSize(self, size):
        pixmap = self.cmdObj.getIconPixmap().scaled(size, Qt.KeepAspectRatio,
                                                    Qt.SmoothTransformation)

        self.ui.label.setPixmap(pixmap)
        self.ui.label.resize(size)

        if self.cmdObj.isVisibleName():
            label = QLabel(self.ui.label)
            label.setText(self.cmdObj.getCommandName())

            labelSize = label.sizeHint()
            parentSize = self.ui.label.size()
            moveX = 0
            moveY = 0

            label.setStyleSheet("background-color:rgba(0,0,0,0.5);")

            if labelSize.width() < parentSize.width():
                moveX = (parentSize.width() - labelSize.width()) / 2 - 4
                label.setStyleSheet(
                    "background-color:rgba(0,0,0,0.5); padding: 0 2px")

            moveY = parentSize.height() - labelSize.height()

            label.move(moveX, moveY)

    def mousePressEvent(self, event):
        self.setStyleSheet("background-color:transparent")
        super(IconWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet(self.defaultStyleSheet)
        super(IconWidget, self).mouseReleaseEvent(event)

    def dragMoveEvent(self, event):
        self.setStyleSheet("background-color:red")
        super(IconWidget, self).dragMoveEvent(event)