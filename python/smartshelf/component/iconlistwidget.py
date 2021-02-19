from PySide2.QtWidgets import QListWidget
from PySide2.QtCore import Qt

from smartshelf.view.iconcreationdialog import IconCreationDialog


class IconListWidget(QListWidget):
    def __init__(self, parent=None):
        super(IconListWidget, self).__init__(parent=parent)

    def createIcon(self, codeText=None, codePath=None):
        iconCreationDialog = IconCreationDialog(self)

        if codeText:
            iconCreationDialog.setCodeText(codeText)
        elif codePath:
            iconCreationDialog.setCodePath(codePath)

        iconCreationDialog.show()

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
                self.createIcon(codePath=path)

        elif event.mimeData().hasText():
            self.createIcon(codeText=event.mimeData().text())

        else:
            super(IconListWidget, self).dropEvent(event)

            if event.dropAction() == Qt.DropAction.MoveAction:
                print "update"
