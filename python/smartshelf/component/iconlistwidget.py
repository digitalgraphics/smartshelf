from PySide2.QtWidgets import QListWidget, QListWidgetItem
from PySide2.QtCore import Qt, Signal, QSize

from smartshelf.component.iconwidget import IconWidget


class IconListWidget(QListWidget):

    fileDropped = Signal(str)
    textDropped = Signal(str)

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

    def addIcon(self, label, pixmap):
        widget = IconWidget(label, pixmap)

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
