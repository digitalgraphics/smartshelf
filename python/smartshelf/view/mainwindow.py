from smartshelf.ui.mainwindow import Ui_mainWindow
from smartshelf.view.iconcreationdialog import IconCreationDialog
from smartshelf.component.iconlistwidget import IconListWidget
from smartshelf.component.commandobject import CommandObject

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
        self.smartshelfHistory = dict()
        self.curIconSize = QSize(32, 32)

        self.initCommands()

    def initCommands(self):
        self.loadLocalRepos()

    def loadLocalRepos(self):
        if not fileUtils.existingPath(self.localRepos):
            fileUtils.createFolder(self.localRepos)
            return

        tabPaths = fileUtils.getFolders(self.localRepos)

        for tabPath in tabPaths:
            tabName = fileUtils.getFolderBaseName(tabPath)
            self.createTab(tabName)
            self.smartshelfHistory[tabName] = dict()

            for codePath in fileUtils.getCodeFilesFromFolder(tabPath):
                iconPath = fileUtils.getCodeThumbnail(codePath)
                commandName = fileUtils.getFileBaseName(codePath,
                                                        withExtension=False)
                commandText = fileUtils.readTextFile(codePath)
                isPythonCode = codePath.endswith(".py")

                cmdObj = CommandObject()
                cmdObj.setFolderPath(tabPath)
                cmdObj.setIconPixmap(QPixmap(iconPath))
                cmdObj.setCommandName(commandName)
                cmdObj.setIsVisibleName(True)
                cmdObj.setCommand(commandText, isPythonCode)

                self.addCommandObjToTab(cmdObj, tabName)

    def createTab(self, tabName):
        iconListWidget = IconListWidget()

        iconListWidget.setIconSize(self.curIconSize)

        iconListWidget.fileDropped.connect(self.fileDropped)
        iconListWidget.textDropped.connect(self.textDropped)
        iconListWidget.commandRemoved.connect(self.commandRemoved)
        iconListWidget.commandEdited.connect(self.commandEdited)

        return self.ui.tabWidget.addTab(iconListWidget, tabName)

    def commandRemoved(self, objList):
        cmdObj = objList[0]

    def commandEdited(self, objList):
        cmdObj = objList[0]

    def textDropped(self, text):
        tabWidget = self.ui.tabWidget
        tabName = tabWidget.tabText(tabWidget.currentIndex())
        self.createIcon(tabName=tabName, codeText=text)

    def fileDropped(self, filePath):
        tabWidget = self.ui.tabWidget
        tabName = tabWidget.tabText(tabWidget.currentIndex())
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

        def commandObjCreated():
            cmdObj = iconCreationDialog.getCommandObject()
            tabName = iconCreationDialog.getTabName()

            fileUtils.saveImage(cmdObj.getIconPixmap(),
                                cmdObj.getCommandName(),
                                cmdObj.getFolderPath())

            fileUtils.saveCode(cmdObj.getCommand(), cmdObj.getCommandName(),
                               cmdObj.getFolderPath(), cmdObj.isPython())

            self.addCommandObjToTab(cmdObj, tabName)

        iconCreationDialog.accepted.connect(lambda: commandObjCreated())

    def getListByTabName(self, tabName):
        tabWidget = self.ui.tabWidget

        for i in range(tabWidget.count()):
            if tabWidget.tabText(i) == tabName:
                return tabWidget.widget(i)

        return None

    def addCommandObjToTab(self, cmdObj, tabName):
        iconListWidget = self.getListByTabName(tabName)

        if not iconListWidget:
            index = self.createTab(tabName)
            iconListWidget = self.ui.tabWidget.widget(index)

        iconListWidget.addIcon(cmdObj)

    def settingsPressed(self):
        pass

    def addIconPressed(self):
        self.createIcon()

    def currentList(self):
        return self.ui.tabWidget.currentWidget()

    def setIconSize(self, size):
        return

        # tabWidget = self.ui.tabWidget

        # for i in range(tabWidget.count()):
        #     iconListWidget = tabWidget.widget(i)

        #     iconListWidget.hide()
        #     iconListWidget.clear()

        #     iconListWidget.setIconSize(size)

        #     for i in range(100):
        #         iconListWidget.addIcon(str(i), QPixmap("C:/Desktop/icon.png"))

        #     iconListWidget.show()