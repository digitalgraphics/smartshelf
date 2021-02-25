from smartshelf.ui.settingsdialog import Ui_settingsDialog
from PySide2.QtWidgets import QDialog, QListWidgetItem, QMessageBox, QInputDialog
from PySide2.QtCore import Qt


class SettingsDialog(QDialog):
    SharedCmds = 0
    PrivateCmds = 1
    AllCmds = 2

    Icon32 = 32
    Icon64 = 64

    ClearOrganisation = 0
    ClearAll = 1
    NoClear = 2

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent=parent)

        self.ui = Ui_settingsDialog()
        self.ui.setupUi(self)

        self.ui.removeTabButton.setEnabled(False)
        self.ui.editTabButton.setEnabled(False)

        self.ui.tabWidget.itemSelectionChanged.connect(
            self.tabSelectionChanged)
        self.ui.addTabButton.clicked.connect(self.addTabClicked)
        self.ui.removeTabButton.clicked.connect(self.removeTabClicked)
        self.ui.editTabButton.clicked.connect(self.renameClicked)
        self.ui.clearOrganisationButton.clicked.connect(
            self.clearOrganisationClicked)
        self.ui.clearAllButton.clicked.connect(self.clearAllClicked)
        self.ui.sharedCmdButton.clicked.connect(self.showRadioAlert)
        self.ui.privateCmdButton.clicked.connect(self.showRadioAlert)
        self.ui.allCmdButton.clicked.connect(self.showRadioAlert)

        self.clearType = self.NoClear

    def showRadioAlert(self):
        QMessageBox.warning(
            self, 'Bug report',
            'Usolved bug: User organisation may be dammaged when changing visibility',
            QMessageBox.StandardButton.Ok)

    def clearAllClicked(self):
        reply = QMessageBox.question(
            self, 'Clear all user modification',
            "Are you sure to delete all user modification", QMessageBox.Yes,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.clearType = self.ClearAll
            self.accept()

    def clearOrganisationClicked(self):
        reply = QMessageBox.question(
            self, 'Clear user organisation',
            "Are you sure to delete the user organisation", QMessageBox.Yes,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.clearType = self.ClearOrganisation
            self.accept()

    def getClearType(self):
        return self.clearType

    def renameClicked(self):
        item = self.ui.tabWidget.currentItem()

        if not item:
            return

        self.ui.tabWidget.editItem(item)

    def removeTabClicked(self):
        item = self.ui.tabWidget.currentItem()

        if not item:
            return

        reply = QMessageBox.question(
            self, 'Delete a tab',
            "Are you sure to delete the tab " + item.text(), QMessageBox.Yes,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.ui.tabWidget.takeItem(self.ui.tabWidget.row(item))

    def tabSelectionChanged(self):
        item = self.ui.tabWidget.currentItem()

        if item and not self.isTabLocked(item.text()):
            self.ui.removeTabButton.setEnabled(True)
            self.ui.editTabButton.setEnabled(True)
        else:
            self.ui.removeTabButton.setEnabled(False)
            self.ui.editTabButton.setEnabled(False)

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

    def addTabClicked(self):
        nameAlreadyExists = True

        while nameAlreadyExists:
            nameWrongFormat = True

            while nameWrongFormat:
                text, ok = QInputDialog.getText(
                    self, 'New tab', "Enter the name of the new tab")

                if not ok:
                    return

                nameWrongFormat = not self.checkName(text)

            nameAlreadyExists = False

            for i in range(self.ui.tabWidget.count()):
                item = self.ui.tabWidget.item(i)
                if item.text() == text:
                    nameAlreadyExists = True
                    QMessageBox.warning(
                        self, 'Existing name',
                        'The tab "' + text + '" already exists',
                        QMessageBox.StandardButton.Ok)

        if ok and text:
            self.appendTab(text)

    def appendTab(self, tabName, isLocked=False):
        item = QListWidgetItem(tabName)
        item.setData(Qt.UserRole, tabName)

        self.ui.tabWidget.insertItem(self.ui.tabWidget.count(), item)
        if not isLocked:
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        else:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setTextColor(Qt.darkGray)

    def getTabs(self):
        tabs = []
        for i in range(self.ui.tabWidget.count()):
            item = self.ui.tabWidget.item(i)
            tabs.append(item.text())

        return tabs

    def getTabOldNames(self):
        tabs = []
        for i in range(self.ui.tabWidget.count()):
            item = self.ui.tabWidget.item(i)
            tabs.append(item.data(Qt.UserRole))

        return tabs

    def isTabLocked(self, tabName):
        for i in range(self.ui.tabWidget.count()):
            item = self.ui.tabWidget.item(i)
            if item.text() == tabName:
                if item.flags() == (item.flags() & ~Qt.ItemIsEditable):
                    return True
                else:
                    return False

    def getTabOldName(self, tabName):
        for i in range(self.ui.tabWidget.count()):
            item = self.ui.tabWidget.item(i)
            if item.text() == tabName:
                return item.data(Qt.UserRole)

        return None

    def setUserSettingsPath(self, path):
        self.ui.settingsPathEdit.setText(path)

    def setIconSize(self, size):
        if size == self.Icon32:
            self.ui.size32Button.setChecked(True)
        else:
            self.ui.size64Button.setChecked(True)

    def getIconSize(self):
        if self.ui.size32Button.isChecked():
            return self.Icon32
        else:
            return self.Icon64

    def setCmdsVisibility(self, visibility):
        if visibility == self.SharedCmds:
            self.ui.sharedCmdButton.setChecked(True)
        elif visibility == self.PrivateCmds:
            self.ui.privateCmdButton.setChecked(True)
        else:
            self.ui.allCmdButton.setChecked(True)

    def getCmdsVisibility(self):
        if self.ui.sharedCmdButton.isChecked():
            return self.SharedCmds
        elif self.ui.privateCmdButton.isChecked():
            return self.PrivateCmds
        else:
            return self.AllCmds

    def isLocalVisible(self):
        if self.ui.privateCmdButton.isChecked(
        ) or self.ui.allCmdButton.isChecked():
            return True
        else:
            return False

    def isSharedVisible(self):
        if self.ui.sharedCmdButton.isChecked(
        ) or self.ui.allCmdButton.isChecked():
            return True
        else:
            return False

    def accept(self):
        super(SettingsDialog, self).accept()