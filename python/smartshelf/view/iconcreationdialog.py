from smartshelf.ui.iconcreationdialog import Ui_iconCreationDialog
from smartshelf.view.iconsearchdialog import IconSearchDialog
from smartshelf.component.commandobject import CommandObject

import smartshelf.utils.file as fileUtils

from PySide2.QtWidgets import QDialog, QGraphicsScene, QInputDialog, QMessageBox, QFileDialog
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QKeySequence

import maya.mel as mel

import copy
import os


class IconCreationDialog(QDialog):
    def __init__(self, reposPath, tabWidget, cmdObj, editing, parent=None):
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

        for i in range(tabWidget.count()):
            self.ui.containingTabComboBox.addItem(tabWidget.tabText(i))

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
            self.setCodeText(cmdObj.getCommand(), force=True)
            self.isPythonCode(cmdObj.isPython())

        if cmdObj.isLocked():
            self.ui.codeTextEdit.setReadOnly(True)
            self.ui.browseFolderButton.setEnabled(False)
            self.ui.browseFavouriteButton.setEnabled(False)
            self.ui.nameEdit.setEnabled(False)
            self.ui.iconThumbnail.setEnabled(False)
            self.ui.containingTabComboBox.setEnabled(False)
            self.ui.addTabButton.setEnabled(False)
            self.ui.pythonButton.setEnabled(False)
            self.ui.melButton.setEnabled(False)

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
            return False

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

    def setCodeText(self, text, force=False):
        if not self.cmdObj.isLocked() or force:
            self.ui.codeTextEdit.setText(text)

    def runPressed(self):
        text = self.ui.codeTextEdit.toPlainText()
        path = self.reposPath + "/" + self.ui.containingTabComboBox.currentText(
        )
        workingDir = os.getcwd()

        if text:
            os.chdir(path)
            try:
                if self.ui.pythonButton.isChecked():
                    exec text in globals(), globals()
                else:
                    mel.eval(text)
            finally:
                os.chdir(workingDir)

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
            self, "Select an image", "",
            "Image files (*.jpg *.gif *.png *.svg)")
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
        currentList = self.parent().getListByTabName(currentTab)
        nameText = self.ui.nameEdit.text()

        if not self.checkName(nameText):
            return

        if not currentTab:
            QMessageBox.warning(self, 'No tab selected',
                                "Please select a destination tab",
                                QMessageBox.StandardButton.Ok)
            return

        folderPath = self.reposPath + "/" + currentTab

        if ((not self.isEditing) and currentList
                and currentList.getItemByName(nameText)) or (
                    self.isEditing and
                    (currentTab != self.oldCmdObj.getContainingTab()
                     or nameText != self.oldCmdObj.getCommandName())
                    and currentList and currentList.getItemByName(nameText)):
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
