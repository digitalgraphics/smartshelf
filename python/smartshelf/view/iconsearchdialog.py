from smartshelf.ui.iconsearchdialog import Ui_iconSearchDialog
from smartshelf.component.iconwidget import IconWidget
from smartshelf.component.commandobject import CommandObject

import smartshelf.utils.file as fileUtils

from PySide2.QtWidgets import QDialog, QGraphicsScene, QListWidgetItem, QPushButton
from PySide2.QtCore import Qt, QSize, QThread, Signal, QObject
from PySide2.QtGui import QPixmap, QKeySequence

import os
import time
import maya.cmds as cmds


class Worker(QObject):
    finished = Signal()
    progress = Signal(str)
    maximumComputed = Signal(int)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent=parent)

    def run(self):
        iconPaths = self.getIconPaths()

        self.maximumComputed.emit(len(iconPaths))

        for iconPath in iconPaths:
            self.progress.emit(iconPath)

        self.finished.emit()

    def getIconPaths(self):
        paths = []

        envNames = ['MAYA_FILE_ICON_PATH', 'XBMLANGPATH']

        for envName in envNames:
            try:
                entries = os.environ[envName]

                for entry in entries.split(";"):
                    paths.append(entry)
            except:
                pass

        iconFiles = []

        for filename in cmds.resourceManager(nameFilter="*"):
            iconFiles.append(":" + filename)

        for path in paths:
            for (dirpath, dirnames, filenames) in os.walk(path):
                for filename in filenames:
                    if filename.endswith('.bmp') or filename.endswith(
                            '.png') or filename.endswith(
                                '.xpm') or filename.endswith('.svg'):
                        iconFiles.append(os.sep.join([dirpath, filename]))

        return iconFiles


class IconSearchDialog(QDialog):
    def __init__(self, parent=None):
        super(IconSearchDialog, self).__init__(parent=parent)
        self.ui = Ui_iconSearchDialog()
        self.ui.setupUi(self)

        self.ui.searchEdit.textChanged.connect(self.searchChanged)
        self.ui.listWidget.itemDoubleClicked.connect(self.itemDoubleClicked)

        self.ui.listWidget.setFocus()
        self.ui.listWidget.setIconSize(QSize(32, 32))

        self.initIcons()

    def initIcons(self):
        self.thread = QThread()

        self.worker = Worker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.worker.maximumComputed.connect(self.setMaxProgressBar)

        self.ui.iconsWidget.hide()
        self.ui.progressBar.setValue(0)
        self.ui.loadingWidget.show()

        self.thread.start()

        self.thread.finished.connect(self.hideProgressBar)

    def setMaxProgressBar(self, value):
        self.ui.progressBar.setMaximum(value)

    def reportProgress(self, path):
        self.addIcon(path)
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)

    def hideProgressBar(self):
        self.ui.loadingWidget.hide()
        self.ui.iconsWidget.show()

    def filterIcons(self, filter):
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            label = item.toolTip()

            if (not filter) or (filter.lower() in label.lower()):
                item.setHidden(False)
            else:
                item.setHidden(True)

    def searchChanged(self, text):
        self.filterIcons(text)

    def addIcon(self, filepath):
        pixmap = QPixmap(filepath)
        label = fileUtils.getFileBaseName(filepath,
                                          withExtension=False).lstrip(":")

        cmdObj = CommandObject()
        cmdObj.setIconPixmap(pixmap)
        cmdObj.setCommandName(label)
        cmdObj.setIsVisibleName(False)

        widget = IconWidget(cmdObj)
        item = QListWidgetItem()

        self.ui.listWidget.insertItem(self.ui.listWidget.count(), item)
        self.ui.listWidget.setItemWidget(item, widget)
        curSize = self.ui.listWidget.iconSize()

        item.setSizeHint(curSize)
        item.setData(Qt.UserRole, filepath)
        item.setToolTip(label)

        widget.setSize(curSize)

    def itemDoubleClicked(self, item):
        print self.getSelectedIconPath()
        self.accept()

    def getSelectedIconPath(self):
        items = self.ui.listWidget.selectedItems()

        if len(items) > 0:
            return items[0].data(Qt.UserRole)
        else:
            return ":mayaIcon.png"

    def accept(self):
        super(IconSearchDialog, self).accept()

    def reject(self):
        super(IconSearchDialog, self).reject()
