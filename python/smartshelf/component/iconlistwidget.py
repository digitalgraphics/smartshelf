from PySide2.QtWidgets import QListWidget, QListWidgetItem, QMenu
from PySide2.QtCore import Qt, Signal, QSize
from PySide2.QtGui import QGuiApplication

from smartshelf.component.iconwidget import IconWidget
from smartshelf.component.commandobject import CommandObject

import smartshelf.utils.mayautils as mayaUtils


class IconListWidget(QListWidget):

    fileDropped = Signal(str)
    textDropped = Signal(str)
    commandRemoved = Signal(list)
    commandEdited = Signal(list)

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
        self.setDragDropMode(self.DragDrop)
        self.setDragEnabled(True)
        self.setEditTriggers(self.NoEditTriggers)
        self.setAcceptDrops(True)
        self.setMinimumSize(QSize(40, 40))

    def contextMenuEvent(self, event):

        item = self.itemAt(event.pos())

        if not item:
            super(IconListWidget, self).contextMenuEvent(event)
            return

        iconWidget = self.itemWidget(item)
        cmdObj = iconWidget.getCommandObject()

        menu = QMenu(self)

        editAction = menu.addAction("Edit")
        copyCodeAction = menu.addAction("Copy code")
        removeAction = menu.addAction("Remove")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == editAction:
            self.commandEdited.emit([cmdObj])

        if action == copyCodeAction:
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(cmdObj.getCommand())
            mayaUtils.printWarning('Code from "' + cmdObj.getCommandName() +
                                   '" is copied into the clipboard')

        if action == removeAction:
            self.takeItem(self.row(item))
            self.commandRemoved.emit([cmdObj])

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.RightButton:
    #         pass

    def addIcon(self, cmdObj):
        widget = IconWidget(cmdObj)
        item = QListWidgetItem()

        self.insertItem(self.count(), item)
        self.setItemWidget(item, widget)

        curSize = self.iconSize()
        item.setSizeHint(curSize)
        widget.setSize(curSize)

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
            super(IconListWidget, self).dropEvent(event)

            if event.dropAction() == Qt.DropAction.MoveAction:
                print "update"
