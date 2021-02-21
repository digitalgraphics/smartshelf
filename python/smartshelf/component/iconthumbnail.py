import importlib
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QIcon, QPixmap, QImage, QFont, QKeySequence
from PySide2.QtCore import QUrl, Qt
from PySide2.QtWidgets import QGraphicsScene, QMessageBox


class IconThumbnail(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(IconThumbnail, self).__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        self.setAcceptDrops(True)
        self.iconPixmap = None

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)

        actionPaste = menu.addAction("Paste")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == actionPaste:
            self.pasteIconFromClipboard()

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste):
            self.pasteIconFromClipboard()

    def pasteIconFromClipboard(self):

        clipboard = QtGui.QGuiApplication.clipboard()

        mime_data = clipboard.mimeData()

        urls = [i for i in mime_data.urls()]

        if len(urls) > 0:
            self.setIconPath(urls[0].toLocalFile())

    def setIconPath(self, path):
        if path.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            self.setIcon(QPixmap(path))
        else:
            QMessageBox.warning(self, 'Wrong file format',
                                "The selected file is not an image",
                                QMessageBox.StandardButton.Ok)

    def setIcon(self, pixmap):

        if pixmap.isNull():
            pixmap = QPixmap(":/icon/mayaLogo.png")

        self.iconPixmap = pixmap

        scene = QGraphicsScene()
        self.setScene(scene)
        scene.addPixmap(pixmap)
        self.fitInView(scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def getIconPixmap(self):
        return self.iconPixmap

    # The following three methods set up dragging and dropping for the app
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Drop files directly onto the widget
        File locations are stored in fname
        :param e:
        :return:
        """
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            urls = event.mimeData().urls()

            if len(urls) > 0:
                self.setIconPath(urls[0].toLocalFile())
        else:
            event.ignore()
