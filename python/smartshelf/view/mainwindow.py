from smartshelf.ui.mainwindow import Ui_mainWindow
from smartshelf.view.iconcreationdialog import IconCreationDialog
from smartshelf.component.iconlistwidget import IconListWidget

from PySide2.QtWidgets import QMainWindow, QWidget, QLabel, QListWidget
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QPixmap, QImage

import smartshelf.utils.file as fileUtils

import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.ui.addButton.buttonPressed.connect(self.addIconPressed)
        self.ui.settingsButton.buttonPressed.connect(self.settingsPressed)

        self.sharedRepos = self.historyPath = [
            s for s in sys.path if 'prefs' in s
        ][0] + "/smartshelfSharedRepository"

        self.localRepos = self.historyPath = [
            s for s in sys.path if 'prefs' in s
        ][0] + "/smartshelfRepository"

        self.initCommands()

    def initCommands(self):
        self.loadLocalRepos()
        self.setIconSize(QSize(32, 32))

    def loadLocalRepos(self):
        if not fileUtils.existingPath(self.localRepos):
            fileUtils.createFolder(self.localRepos)
            return

        tabPaths = fileUtils.getFolders(self.localRepos)

        for tabPath in tabPaths:
            tabName = fileUtils.getFolderBaseName(tabPath)
            self.createTab(tabName)

    def createTab(self, tabName):
        iconListWidget = IconListWidget()

        iconListWidget.fileDropped.connect(self.fileDropped)
        iconListWidget.textDropped.connect(self.textDropped)

        self.ui.tabWidget.addTab(iconListWidget, tabName)

    def textDropped(self, text):
        tabName = self.ui.tabWidget.tabText(self.ui.currentIndex())
        self.createIcon(tabName=tabName, codeText=text)

    def fileDropped(self, filePath):
        tabName = self.ui.tabWidget.tabText(self.ui.currentIndex())
        self.createIcon(tabName=tabName, codePath=filePath)

    def createIcon(self, tabName=None, codeText=None, codePath=None):
        tabWidget = self.ui.tabWidget
        tabLabels = []

        for i in range(tabWidget.count()):
            tabLabels.append(tabWidget.tabText(i))

        iconCreationDialog = IconCreationDialog(self.localRepos, tabLabels,
                                                self)

        if tabName:
            iconCreationDialog.setTabName(tabName)
        elif codeText:
            iconCreationDialog.setCodeText(codeText)
        elif codePath:
            iconCreationDialog.setCodePath(codePath)

        iconCreationDialog.show()

        def commandObjCreated(ref):
            print ref
            cmdObj = iconCreationDialog.getCommandObject()
            tabName = iconCreationDialog.getTabName()
            ref.addCommandObjToTab(cmdObj, tabName)

        iconCreationDialog.accepted.connect(lambda: commandObjCreated(self))

    def addCommandObjToTab(self, cmdObj, tabName):
        print "coucou"

    def settingsPressed(self):
        pass

    def addIconPressed(self):
        self.createIcon()

    def currentList(self):
        return self.ui.tabWidget.currentWidget()

    def setIconSize(self, size):
        return

        tabWidget = self.ui.tabWidget

        for i in range(tabWidget.count()):
            iconListWidget = tabWidget.widget(i)

            iconListWidget.hide()
            iconListWidget.clear()

            iconListWidget.setIconSize(size)

            for i in range(100):
                iconListWidget.addIcon(str(i), QPixmap("C:/Desktop/icon.png"))

            iconListWidget.show()