import importlib
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QIcon, QPixmap, QImage, QFont, QKeySequence
from PySide2.QtCore import QUrl, Qt
from PySide2.QtWidgets import QPlainTextEdit, QMessageBox

from smartshelf.component.pythonhighlighter import PythonHighlighter


class CodePlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(CodePlainTextEdit, self).__init__(parent)

        self.setAcceptDrops(True)

        font = QFont()
        font.setFixedPitch(True)
        self.setFont(font)

        self.isPython = None
        self.curHighlighter = PythonHighlighter(None)

        self.setPythonCode()

    def setPythonCode(self):
        self.isPython = True
        self.curHighlighter.setDocument(self.document())

    def setMelCode(self):
        self.isPython = False
        self.curHighlighter.setDocument(None)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            p = self.textCursor().position()
            result = self.toPlainText()[:p]
            lastLine = result.split("\n")[-1]
            nbTabs = lastLine.count("\t")

            super(CodePlainTextEdit, self).keyPressEvent(event)

            if self.isPython and result.rstrip().endswith(":"):
                nbTabs += 1
            elif (not self.isPython) and result.rstrip().endswith("{"):
                nbTabs += 1

            self.insertPlainText('\t' * nbTabs)
            return

        super(CodePlainTextEdit, self).keyPressEvent(event)

    def pasteFromClipboard(self):

        clipboard = QtGui.QGuiApplication.clipboard()

        mime_data = clipboard.mimeData()

        urls = [i for i in mime_data.urls()]

        if len(urls) > 0:
            self.setTextfilePath(urls[0].toLocalFile())

    def setTextfilePath(self, path):
        if path.lower().endswith(('.txt', '.py', '.mel', '.json')):
            self.setTextfile(path)
        else:
            QMessageBox.warning(self, 'Wrong file format',
                                "The selected file is not a text file",
                                QMessageBox.StandardButton.Ok)

    def setTextfile(self, path):
        text = ''.join(open(path).readlines())
        self.setText(text)

    def setText(self, text):
        self.setPlainText(text)

    def getText(self):
        return self.toPlainText()

    # The following three methods set up dragging and dropping for the app
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasUrls:
            urls = event.mimeData().urls()

            if len(urls) > 0:
                self.setTextfilePath(urls[0].toLocalFile())

        elif event.mimeData().hasText():
            self.setText(event.mimeData().text())

        else:
            event.ignore()