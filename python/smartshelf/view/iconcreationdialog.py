from smartshelf.ui.iconcreationdialog import Ui_iconCreationDialog

from PySide2.QtWidgets import QDialog, QGraphicsScene
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QKeySequence

import maya.mel as mel


class IconCreationDialog(QDialog):
    def __init__(self, parent=None):
        super(IconCreationDialog, self).__init__(parent=parent)
        self.ui = Ui_iconCreationDialog()
        self.ui.setupUi(self)

        self.ui.browseFolderButton.buttonPressed.connect(
            self.browseFolderPressed)
        self.ui.melButton.pressed.connect(self.melPressed)
        self.ui.pythonButton.pressed.connect(self.pythonPressed)
        self.ui.runButton.pressed.connect(self.runPressed)

        self.show()

        self.ui.iconThumbnail.setIcon(QPixmap("C:/Pictures/noro.png"))

    def setCodeText(self, text):
        self.ui.codeTextEdit.setText(text)

    def setCodePath(self, filepath):
        self.ui.codeTextEdit.setTextfile(filepath)

    def runPressed(self):
        text = self.ui.codeTextEdit.toPlainText()

        if text:
            if self.ui.pythonButton.isChecked():
                exec(text)
            else:
                mel.eval(text)

    def pythonPressed(self):
        self.ui.codeTextEdit.setPythonCode()

    def melPressed(self):
        self.ui.codeTextEdit.setMelCode()

    def browseFolderPressed(self):
        self.ui.iconThumbnail.setIcon(QPixmap("C:/Pictures/noro.png"))

    def keyPressEvent(self, event):
        if ((event.modifiers() and Qt.ControlModifier) and
            (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter
             or event.key() == Qt.Key_Space)):
            self.runPressed()
