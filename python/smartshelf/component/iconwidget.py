from smartshelf.ui.iconwidget import Ui_iconWidget

from PySide2.QtWidgets import QMainWindow, QListWidgetItem, QWidget, QLabel
from PySide2.QtCore import QSize, Qt, QPoint
from PySide2.QtGui import QIcon, QPixmap, QImage, QFont


class IconWidget(QWidget):
    def __init__(self, text, pixmap, showLabel=False, parent=None):
        super(IconWidget, self).__init__(parent=parent)
        self.ui = Ui_iconWidget()
        self.ui.setupUi(self)

        self.pixmap = pixmap
        self.text = text
        self.showLabel = showLabel

        self.setToolTip(self.text)
        self.defaultStyleSheet = self.styleSheet()

    def setSize(self, size):
        pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)

        self.ui.label.setPixmap(pixmap)

        self.ui.label.resize(size)

        label = QLabel(self.ui.label)

        if self.showLabel:
            label.setText(self.text)

        label.resize(size)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

    def mousePressEvent(self, event):
        self.setStyleSheet("background-color:transparent")
        super(IconWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet(self.defaultStyleSheet)
        super(IconWidget, self).mouseReleaseEvent(event)

    def dragMoveEvent(self, event):
        self.setStyleSheet("background-color:red")
        super(IconWidget, self).dragMoveEvent(event)