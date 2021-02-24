from smartshelf.ui.mainwindow import Ui_mainWindow
from smartshelf.view.iconcreationdialog import IconCreationDialog
from smartshelf.component.iconlistwidget import IconListWidget
from smartshelf.component.commandobject import CommandObject

from PySide2.QtWidgets import QMainWindow, QWidget, QLabel, QListWidget
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QPixmap, QImage

import smartshelf.utils.file as fileUtils
import maya.mel as mel

import sys
import copy


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.ui.addButton.buttonPressed.connect(self.addIconPressed)
        self.ui.settingsButton.buttonPressed.connect(self.settingsPressed)

        self.sharedRepos = "H:/sandbox/raphaelJ/smartshelf_shared_repository"

        self.localRepos = self.historyPath = [
            s for s in sys.path if 'prefs' in s
        ][0] + "/smartshelfRepository"
        self.smartshelfHistory = dict()
        self.curIconSize = QSize(32, 32)

        self.initCommands()

    def initCommands(self):
        self.loadSharedRepos()
        self.loadLocalRepos()
        self.currentList().appendSeparator()

    def loadSharedRepos(self):
        self.loadRepos(self.sharedRepos)

    def loadLocalRepos(self):
        if not fileUtils.existingPath(self.localRepos):
            fileUtils.createFolder(self.localRepos)
            return

        self.loadRepos(self.localRepos)

    def loadRepos(self, reposPath):
        if not fileUtils.existingPath(reposPath):
            return

        tabPaths = fileUtils.getFolders(reposPath)

        for tabPath in tabPaths:
            tabName = fileUtils.getFolderBaseName(tabPath)

            if not self.getListByTabName(tabName):
                self.createTab(tabName)

            self.smartshelfHistory[tabName] = dict()

            for codePath in fileUtils.getCodeFilesFromFolder(tabPath):
                for i in range(5):
                    iconPath = fileUtils.getCodeThumbnail(codePath)
                    commandName = fileUtils.getFileBaseName(codePath,
                                                            withExtension=False)
                    commandText = fileUtils.readTextFile(codePath)
                    isPythonCode = codePath.endswith(".py")

                    cmdObj = CommandObject()
                    cmdObj.setFolderPath(tabPath)
                    cmdObj.setIconPixmap(QPixmap(iconPath))
                    cmdObj.setCommandName(commandName + str(i))
                    cmdObj.setIsVisibleName(True)
                    cmdObj.setContainingTab(tabName)
                    cmdObj.setCommand(commandText, isPythonCode)

                    self.addCommandObjToTab(cmdObj, tabName)

    def createTab(self, tabName):
        folderPath = self.localRepos + "/" + tabName

        if not fileUtils.existingPath(folderPath):
            fileUtils.createFolder(folderPath)

        iconListWidget = IconListWidget()

        iconListWidget.setIconSize(self.curIconSize)

        iconListWidget.fileDropped.connect(self.fileDropped)
        iconListWidget.textDropped.connect(self.textDropped)
        iconListWidget.commandRemoved.connect(self.commandRemoved)
        iconListWidget.commandEdited.connect(self.commandEdited)
        iconListWidget.itemClicked.connect(self.commandClicked)

        return self.ui.tabWidget.addTab(iconListWidget, tabName)

    def commandClicked(self, item):
        iconList = item.listWidget()
        widget = iconList.itemWidget(item)
        cmdObj = widget.getCommandObject()
        self.runCommand(cmdObj)

    def runCommand(self, cmdObj):
        text = cmdObj.getCommand()

        if text:
            if cmdObj.isPython():
                exec(text)
            else:
                mel.eval(text)

    def commandRemoved(self, objList):
        cmdObj = objList[0]
        self.removeIconFromFile(cmdObj)
        self.removeIconFromList(cmdObj)

    def commandEdited(self, objList):
        cmdObj = objList[0]
        self.createIcon(cmdObj, editing=True)

    def textDropped(self, text):
        cmdObj = CommandObject()
        cmdObj.setContainingTab(self.currentTabName())
        cmdObj.setCommand(text)
        self.createIcon(cmdObj=cmdObj)

    def fileDropped(self, filePath):
        cmdObj = CommandObject()
        cmdObj.setContainingTab(self.currentTabName())
        cmdObj.setCommand(fileUtils.readTextFile(filePath))
        self.createIcon(cmdObj=cmdObj)

    def removeIconFromFile(self, cmdObj):
        folderPath = cmdObj.getFolderPath()
        tabName = cmdObj.getContainingTab()
        commandName = cmdObj.getCommandName()
        isPythonCode = cmdObj.isPython()

        path = folderPath + "/" + commandName

        if isPythonCode:
            path += ".py"
        else:
            path += ".mel"

        fileUtils.removeCodeFiles([path])

    def removeIconFromList(self, cmdObj, tabName=None):
        if not tabName:
            tabName = cmdObj.getContainingTab()
        commandName = cmdObj.getCommandName()
        iconList = self.getListByTabName(tabName)
        iconList.removeIcon(commandName)

    def moveCmdObj(self, oldCmdObj, cmdObj):
        self.addCommandObjToTab(cmdObj, cmdObj.getContainingTab())
        self.removeIconFromFile(oldCmdObj)
        self.removeIconFromList(oldCmdObj, oldCmdObj.getContainingTab())

    def updateCmdObj(self, oldCmdObj, cmdObj):
        iconList = self.getListByTabName(cmdObj.getContainingTab())
        iconList.updateIcon(oldCmdObj.getCommandName())
        self.removeIconFromFile(oldCmdObj)

    def createIcon(self, cmdObj=None, editing=False):
        tabWidget = self.ui.tabWidget
        tabLabels = []
        oldCmdObj = copy.deepcopy(cmdObj)

        for i in range(tabWidget.count()):
            tabLabels.append(tabWidget.tabText(i))

        if not cmdObj:
            cmdObj = CommandObject()

        # open the dialog to create/modify an icon
        iconCreationDialog = IconCreationDialog(self.localRepos, tabLabels, cmdObj,  editing,
                                                self)

        iconCreationDialog.show()

        def commandObjCreated():

            cmdObj = iconCreationDialog.getCommandObject()
            tabName = iconCreationDialog.getTabName()

            # creation
            if not editing:
                self.addCommandObjToTab(cmdObj, tabName)
            # editing with other directory
            elif oldCmdObj.getFolderPath() != cmdObj.getFolderPath():
                self.moveCmdObj(oldCmdObj,
                                cmdObj)
            # editing with other name
            else:
                self.updateCmdObj(oldCmdObj,
                                  cmdObj)

            fileUtils.saveImage(cmdObj.getIconPixmap(),
                                cmdObj.getCommandName(),
                                cmdObj.getFolderPath())

            fileUtils.saveCode(cmdObj.getCommand(), cmdObj.getCommandName(),
                               cmdObj.getFolderPath(), cmdObj.isPython())

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

        iconListWidget.appendIcon(cmdObj)

    def settingsPressed(self):
        pass

    def addIconPressed(self):
        cmdObj = CommandObject()
        cmdObj.setContainingTab(self.currentTabName())
        self.createIcon(cmdObj)

    def currentTabName(self):
        return self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())

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
