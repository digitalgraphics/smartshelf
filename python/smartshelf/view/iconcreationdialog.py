from smartshelf.ui.iconcreationdialog import Ui_iconCreationDialog
from smartshelf.view.iconsearchdialog import IconSearchDialog
from smartshelf.component.commandobject import CommandObject

import smartshelf.utils.file as fileUtils

from PySide2.QtWidgets import QDialog, QGraphicsScene, QInputDialog, QMessageBox, QFileDialog
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QKeySequence

import maya.mel as mel

import copy


class IconCreationDialog(QDialog):
    def __init__(self, reposPath, tabLabels, cmdObj, editing, parent=None):
        super(IconCreationDialog, self).__init__(parent=parent)
        self.ui = Ui_iconCreationDialog()
        self.ui.setupUi(self)

        self.ui.browseFolderButton.buttonPressed.connect(
            self.browseFolderPressed)
        self.ui.browseFavouriteButton.buttonPressed.connect(
            self.browseFavouritePressed)
        self.ui.melButton.pressed.connect(self.melPressed)
        self.ui.pythonButton.pressed.connect(self.pythonPressed)
        self.ui.runButton.pressed.connect(self.runPressed)
        self.ui.addTabButton.buttonPressed.connect(self.addTabPressed)

        self.ui.containingTabComboBox.addItems(tabLabels)
        self.show()
        self.isEditing = editing
        self.iconPath = None
        self.reposPath = reposPath
        self.cmdObj = cmdObj
        self.oldCmdObj = copy.deepcopy(cmdObj)

        if cmdObj.getIconPixmap():
            self.setIconPixmap(cmdObj.getIconPixmap())
        else:
            self.setIconPixmap(QPixmap(":/icon/mayaLogo.png"))

        if cmdObj.getCommandName():
            self.setCommandName(cmdObj.getCommandName())
            self.setCommandNameVisible(cmdObj.isVisibleName())

        if cmdObj.getContainingTab():
            self.setTabName(cmdObj.getContainingTab())

        if cmdObj.getCommand():
            self.setCodeText(cmdObj.getCommand())
            self.isPythonCode(cmdObj.isPython())

    def checkName(self, name):
        def isAscii(text):
            try:
                text.encode('ascii')
            except UnicodeEncodeError:
                return False
            else:
                return True

        if not name:
            QMessageBox.warning(self, 'Wrong name format',
                                'The name cannot be empty',
                                QMessageBox.StandardButton.Ok)
            return False

        if not isAscii(name):
            QMessageBox.warning(self, 'Wrong name format',
                                'The name cannot contain special character',
                                QMessageBox.StandardButton.Ok)
            return False

        if not name[0].isalpha():
            QMessageBox.warning(self, 'Wrong name format',
                                'The name must start with a letter',
                                QMessageBox.StandardButton.Ok)
            False

        return True

    def addTabPressed(self):
        nameAlreadyExists = True
        comboBox = self.ui.containingTabComboBox

        while nameAlreadyExists:
            nameWrongFormat = True

            while nameWrongFormat:
                text, ok = QInputDialog.getText(
                    self, 'New tab', "Enter the name of the new tab")

                if not ok:
                    return

                nameWrongFormat = not self.checkName(text)

            nameAlreadyExists = False

            for i in range(comboBox.count()):
                if comboBox.itemText(i) == text:
                    nameAlreadyExists = True
                    QMessageBox.warning(
                        self, 'Existing name',
                        'The tab "' + text + '" already exists',
                        QMessageBox.StandardButton.Ok)

        if ok and text:
            comboBox.addItem(text)
            comboBox.setCurrentText(text)

    def setIconPixmap(self, pixmap):
        self.ui.iconThumbnail.setIcon(pixmap)

    def setCommandName(self, name):
        self.ui.nameEdit.setText(name)

    def setCommandNameVisible(self, state):
        self.ui.visibleCheckBox.setChecked(state)

    def setTabName(self, tabName):
        self.ui.containingTabComboBox.setCurrentText(tabName)

    def setCodeText(self, text):
        self.ui.codeTextEdit.setText(text)

    def runPressed(self):
        text = self.ui.codeTextEdit.toPlainText()

        if text:
            if self.ui.pythonButton.isChecked():
                exec(text)
            else:
                mel.eval(text)

    def isPythonCode(self, state):
        if state:
            self.ui.pythonButton.setChecked(True)
            self.ui.melButton.setChecked(False)
            self.ui.codeTextEdit.setPythonCode()
        else:
            self.ui.pythonButton.setChecked(False)
            self.ui.melButton.setChecked(True)
            self.ui.codeTextEdit.setMelCode()

    def pythonPressed(self):
        self.isPythonCode(True)

    def melPressed(self):
        self.isPythonCode(False)

    def browseFolderPressed(self):
        path = QFileDialog.getOpenFileName(
            self, "Select an image", "", "Image files (*.jpg *.gif *.png *.svg)")
        if not path:
            return
        else:
            self.iconPath = path[0]
            self.ui.iconThumbnail.setIcon(QPixmap(self.iconPath))

    def browseFavouritePressed(self):
        iconSearchDialog = IconSearchDialog(self)
        if iconSearchDialog.exec_():
            self.iconPath = iconSearchDialog.getSelectedIconPath()
            self.ui.iconThumbnail.setIcon(QPixmap(self.iconPath))

    def keyPressEvent(self, event):
        if ((event.modifiers() and Qt.ControlModifier) and
            (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter
             or event.key() == Qt.Key_Space)):
            self.runPressed()

    def accept(self):
        currentTab = self.ui.containingTabComboBox.currentText()
        nameText = self.ui.nameEdit.text()

        if not self.checkName(nameText):
            return

        folderPath = self.reposPath + "/" + currentTab
        iconPath = folderPath + "/" + nameText + ".png"

        if ((not self.isEditing) and fileUtils.existingPath(folderPath) and fileUtils.existingPath(iconPath)) or (self.isEditing and (currentTab != self.oldCmdObj.getContainingTab() or nameText != self.oldCmdObj.getCommandName()) and fileUtils.existingPath(folderPath) and fileUtils.existingPath(iconPath)):
            QMessageBox.warning(
                self, 'Existing name', 'A script named ' + nameText +
                " already exists in tab " + currentTab,
                QMessageBox.StandardButton.Ok)
            return

        iconPixmap = self.ui.iconThumbnail.getIconPixmap()
        iconPixmap = iconPixmap.scaled(QSize(64, 64), Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)

        self.cmdObj.setFolderPath(folderPath)
        self.cmdObj.setIconPixmap(iconPixmap)
        self.cmdObj.setContainingTab(currentTab)
        self.cmdObj.setCommandName(nameText)
        self.cmdObj.setIsVisibleName(self.ui.visibleCheckBox.isChecked())
        self.cmdObj.setCommand(self.ui.codeTextEdit.getText(),
                               self.ui.pythonButton.isChecked())

        super(IconCreationDialog, self).accept()

    def getCommandObject(self):
        return self.cmdObj

    def getTabName(self):
        return self.ui.containingTabComboBox.currentText()
