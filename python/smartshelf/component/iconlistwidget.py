from PySide2.QtWidgets import QListWidget, QListWidgetItem, QMenu, QFrame
from PySide2.QtCore import Qt, Signal, QSize, QDataStream, QIODevice
from PySide2.QtGui import QGuiApplication, QIcon

from smartshelf.component.iconwidget import IconWidget
from smartshelf.component.commandobject import CommandObject

import smartshelf.utils.mayautils as mayaUtils

import copy
import random
import string


def getRandomString(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class IconListWidget(QListWidget):

    fileDropped = Signal(str)
    textDropped = Signal(str)
    commandRemoved = Signal(list)
    commandEdited = Signal(list)
    commandMoved = Signal()

    def __init__(self, parent=None):
        super(IconListWidget, self).__init__(parent=parent)

        self.setStyleSheet("""
        QListWidget::item {
            border: none;
            outline: 0;
        }

        QListWidget::item:selected {
            background-color: transparent;
        }

        QListWidget{
            border: none;
            outline: 0;
            background-color: transparent;
        }
        """)

        self.setViewMode(self.ListMode)
        self.setSpacing(3)
        self.setResizeMode(self.Adjust)
        self.setWrapping(True)
        self.setFlow(self.LeftToRight)
        self.setMovement(self.Free)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropMode(self.InternalMove)
        self.setDragEnabled(True)
        self.setEditTriggers(self.NoEditTriggers)
        self.setAcceptDrops(True)
        self.setMinimumSize(QSize(40, 40))

        self.isDropping = False
        self.droppedElem = None

        self.model().rowsInserted.connect(self.onRowsInserted)

    def onRowsInserted(self, parentIndex, start, end):
        if self.isDropping and self.droppedElem:
            self.isDropping = False
            self.removeItemIndex(start)

            if isinstance(self.droppedElem, QFrame):
                self.addSeparator(start)
            else:
                self.addIcon(self.droppedElem, start)

            self.droppedElem = None

    def contextMenuEvent(self, event):

        pos = event.pos()
        item = self.itemAt(pos)
        widget = self.itemWidget(item)

        if item:
            if isinstance(widget, QFrame):
                self.contextMenuSeparator(pos)
            else:
                self.contextMenuIcon(pos)
        else:
            self.contextMenuList(pos)

        super(IconListWidget, self).contextMenuEvent(event)
        return

    def contextMenuSeparator(self, pos):
        item = self.itemAt(pos)

        if not item:
            return

        menu = QMenu(self)

        removeSeparatorAction = menu.addAction("Remove")

        action = menu.exec_(self.mapToGlobal(pos))

        if action == removeSeparatorAction:
            self.removeItem(item)
            self.commandMoved.emit()

    def contextMenuList(self, pos):
        menu = QMenu(self)

        addSeparatorAction = menu.addAction("Add Separator")

        action = menu.exec_(self.mapToGlobal(pos))

        if action == addSeparatorAction:
            self.appendSeparator()
            self.commandMoved.emit()

    def contextMenuIcon(self, pos):
        item = self.itemAt(pos)

        if not item:
            return

        iconWidget = self.itemWidget(item)
        cmdObj = iconWidget.getCommandObject()

        menu = QMenu(self)

        editAction = menu.addAction("Edit")
        copyCodeAction = menu.addAction("Copy code")

        isNameVisible = cmdObj.isVisibleName()

        textInfo = "Show the name"
        if isNameVisible:
            textInfo = "Hide the name"

        toggleNameAction = menu.addAction(textInfo)

        addSeparatorAction = menu.addMenu("Add separator")
        separatorBeforeAction = addSeparatorAction.addAction("before icon")
        separatorAfterAction = addSeparatorAction.addAction("after icon")
        removeAction = menu.addAction("Remove")

        if cmdObj.isLocked():
            editAction.setIcon(QIcon(":lock.png"))
            editAction.setEnabled(False)
            removeAction.setIcon(QIcon(":lock.png"))
            removeAction.setEnabled(False)

        action = menu.exec_(self.mapToGlobal(pos))

        if action == editAction:
            self.commandEdited.emit([cmdObj])

        if action == copyCodeAction:
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(cmdObj.getCommand())
            mayaUtils.printWarning('Code from "' + cmdObj.getCommandName() +
                                   '" is copied into the clipboard')

        if action == removeAction:
            self.takeItem(self.indexOfItem(item))
            self.commandRemoved.emit([cmdObj])

        if action == separatorBeforeAction:
            self.addSeparator(self.indexOfItem(item))
            self.commandMoved.emit()

        if action == separatorAfterAction:
            self.addSeparator(self.indexOfItem(item) + 1)
            self.commandMoved.emit()

        if action == toggleNameAction:
            cmdObj.setIsVisibleName(not isNameVisible)
            iconWidget.updateCmdObj()
            self.commandMoved.emit()

    def addIcon(self, cmdObj, pos):
        widget = IconWidget(cmdObj)
        item = QListWidgetItem()

        self.insertItem(pos, item)
        self.setItemWidget(item, widget)

        curSize = self.iconSize()
        item.setSizeHint(curSize)
        widget.setSize(curSize)

    def addSeparator(self, pos):
        curSize = self.iconSize()

        line = QFrame()
        line.setGeometry(0, 0, curSize.width(), curSize.height())
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        item = QListWidgetItem()

        self.insertItem(pos, item)
        self.setItemWidget(item, line)

        item.setSizeHint(curSize)

    def removeAllSeparators(self):
        for i in reversed(range(self.count())):
            item = self.item(i)
            widget = self.itemWidget(item)

            if isinstance(widget, QFrame):
                self.removeItem(item)

    def appendIcon(self, cmdObj):
        self.addIcon(cmdObj, self.count())

    def appendSeparator(self):
        self.addSeparator(self.count())

    def updateIcon(self, oldName):
        item = self.getItemByName(oldName)
        widget = self.itemWidget(item)
        widget.updateCmdObj()

    def getItemByName(self, name):
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            if widget and widget.toolTip() == name:
                return item
        return None

    def indexOfItem(self, item):
        return self.row(item)

    def moveItemToIndex(self, item, index):
        cloneItem = item.clone()
        widget = self.itemWidget(item)

        self.insertItem(index, cloneItem)
        self.setItemWidget(cloneItem, widget)

        self.removeItem(item)

    def removeItemIndex(self, i):
        item = self.item(i)
        self.removeItem(item)

    def removeItem(self, item):
        if item:
            self.takeItem(self.row(item))

    def removeIcon(self, iconName):
        itemToRemove = self.getItemByName(iconName)

        if itemToRemove:
            self.takeItem(self.row(itemToRemove))

    # The following three methods set up dragging and dropping for the app
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.accept()
        else:
            super(IconListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):

        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.accept()
        else:
            super(IconListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()

            if len(urls) > 0:
                path = urls[0].toLocalFile()
                self.fileDropped.emit(path)

        elif event.mimeData().hasText():
            self.textDropped.emit(event.mimeData().text())

        else:
            if event.dropAction() == Qt.DropAction.MoveAction:
                droppedItem = self.currentItem()
                droppedWidget = self.itemWidget(droppedItem)

                # a separator is dropped
                if isinstance(droppedWidget, QFrame):
                    self.droppedElem = QFrame()

                # an icon is dropped
                else:
                    cmdObj = droppedWidget.getCommandObject()
                    self.droppedElem = CommandObject()
                    self.droppedElem.readData(cmdObj)

                self.isDropping = True
                super(IconListWidget, self).dropEvent(event)
                self.commandMoved.emit()
                self.isDropping = False
            else:
                super(IconListWidget, self).dropEvent(event)
