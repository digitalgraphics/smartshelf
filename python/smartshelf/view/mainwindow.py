from smartshelf.ui.mainwindow import Ui_mainWindow
from smartshelf.component.iconwidget import IconWidget

from PySide2.QtWidgets import QMainWindow, QListWidgetItem, QWidget, QLabel, QListWidget
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QPixmap, QImage

from smartshelf.view.iconsearchdialog import IconSearchDialog


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.ui.addButton.buttonPressed.connect(self.addIconPressed)
        self.ui.settingsButton.buttonPressed.connect(self.settingsPressed)

        self.list = self.ui.listWidget

        self.setIconSize(QSize(32, 32))

    def addIcon(self, label, pixmap):
        widget = IconWidget(label, pixmap)

        item = QListWidgetItem()

        self.list.insertItem(self.list.count(), item)
        self.list.setItemWidget(item, widget)
        curSize = self.list.iconSize()
        item.setSizeHint(curSize)
        widget.setSize(curSize)

    def settingsPressed(self):
        iconSearchDialog = IconSearchDialog(self)
        if iconSearchDialog.exec_():
            print iconSearchDialog.getSelectedIconPath()

    def addIconPressed(self):
        self.currentList().createIcon()

    def currentList(self):
        tab = self.ui.tabWidget.currentWidget()
        return tab.findChild(QListWidget)

    def setIconSize(self, size):
        self.list.hide()
        self.list.clear()

        self.list.setIconSize(size)

        for i in range(100):
            self.addIcon(str(i), QPixmap("C:/Desktop/icon.png"))

        self.list.show()