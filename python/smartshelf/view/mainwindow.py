from smartshelf.ui.mainwindow import Ui_mainWindow
from smartshelf.view.iconcreationdialog import IconCreationDialog
from smartshelf.component.iconlistwidget import IconListWidget
from smartshelf.component.commandobject import CommandObject

from PySide2.QtWidgets import QMainWindow, QWidget, QLabel, QListWidget, QFrame, QApplication
from PySide2.QtCore import QSize, Qt, QTimer
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

        self.sharedRepos = "D:/Documents/maya/2019/prefs/scripts/smartshelf_shared_repository"
        # self.sharedRepos = "H:/sandbox/raphaelJ/smartshelf_shared_repository"

        self.localRepos = self.historyPath = [
            s for s in sys.path if 'prefs' in s
        ][0] + "/smartshelfRepository"

        self.sharedReposSettings = self.sharedRepos + "/smartshelf_settings.json"
        self.localReposSettings = self.localRepos + "/smartshelf_settings.json"

        self.smartshelfSettings = dict()
        self.curIconSize = QSize(32, 32)

        self.initCommands()

    def initCommands(self):
        self.loadSharedRepos()
        self.loadLocalRepos()
        self.saveSmartshelfSettings()

    def loadSharedRepos(self):
        self.loadRepos(self.sharedRepos, locked=True)
        self.loadSettings(self.sharedReposSettings)

    def loadLocalRepos(self):
        if not fileUtils.existingPath(self.localRepos):
            fileUtils.createFolder(self.localRepos)
            return

        self.loadRepos(self.localRepos)
        self.loadSettings(self.localReposSettings)

    def loadSettings(self, settingsPath):
        self.smartshelfSettings = fileUtils.readJsonFile(settingsPath)

        if not self.smartshelfSettings:
            return

        for key in self.smartshelfSettings["tabs"]:
            jsonIconList = self.smartshelfSettings["tabs"][key]
            iconList = self.getListByTabName(key)

            if iconList:
                iconList.removeAllSeparators()

                for i in range(len(jsonIconList)):
                    jsonIcon = jsonIconList[i]
                    if jsonIcon["isSeparator"]:
                        iconList.addSeparator(i)
                    else:
                        item = iconList.getItemByName(jsonIcon["name"])
                        if item:
                            widget = iconList.itemWidget(item)
                            cmdObj = widget.getCommandObject()
                            cmdObj.setIsVisibleName(jsonIcon["isNameVisible"])

                            widget.updateCmdObj()

                            iconList.moveItemToIndex(item, i)

    def loadRepos(self, reposPath, locked=False):
        if not fileUtils.existingPath(reposPath):
            return

        tabPaths = fileUtils.getFolders(reposPath)

        for tabPath in tabPaths:
            tabName = fileUtils.getFolderBaseName(tabPath)

            if not self.getListByTabName(tabName):
                self.createTab(tabName)

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
                cmdObj.setContainingTab(tabName)
                cmdObj.setCommand(commandText, isPythonCode)
                cmdObj.setIsLocked(locked)

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
        iconListWidget.commandMoved.connect(self.commandMoved)
        iconListWidget.itemClicked.connect(self.commandClicked)

        return self.ui.tabWidget.addTab(iconListWidget, tabName)

    def saveSmartshelfSettings(self):
        tabWidget = self.ui.tabWidget

        self.smartshelfSettings["tabs"] = dict()

        for i in range(tabWidget.count()):
            iconList = tabWidget.widget(i)

            curIcons = []

            for j in range(iconList.count()):
                item = iconList.item(j)
                widget = iconList.itemWidget(item)

                if isinstance(widget, QFrame):
                    curIcons.append({"name": "separator", "isSeparator": True})
                else:
                    cmdObj = widget.getCommandObject()
                    curIcons.append({
                        "name": cmdObj.getCommandName(),
                        "isNameVisible": cmdObj.isVisibleName(),
                        "isSeparator": False
                    })

            tabName = self.getTabNameList(iconList)
            self.smartshelfSettings["tabs"][tabName] = curIcons

        fileUtils.writeJsonFile(self.smartshelfSettings,
                                self.localReposSettings)

    def commandMoved(self):
        QTimer.singleShot(100, self.saveSmartshelfSettings)

    def commandClicked(self, item):
        iconList = item.listWidget()
        widget = iconList.itemWidget(item)

        if not isinstance(widget, QFrame):
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

        self.saveSmartshelfSettings()

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
        oldCmdObj = copy.deepcopy(cmdObj)

        if not cmdObj:
            cmdObj = CommandObject()

        # open the dialog to create/modify an icon
        iconCreationDialog = IconCreationDialog(self.localRepos, tabWidget,
                                                cmdObj, editing, self)

        iconCreationDialog.show()

        def commandObjCreated():

            cmdObj = iconCreationDialog.getCommandObject()
            tabName = iconCreationDialog.getTabName()

            # creation
            if not editing:
                self.addCommandObjToTab(cmdObj, tabName)
            # editing with other directory
            elif oldCmdObj.getFolderPath() != cmdObj.getFolderPath():
                self.moveCmdObj(oldCmdObj, cmdObj)
            # editing with other name
            else:
                self.updateCmdObj(oldCmdObj, cmdObj)

            fileUtils.saveImage(cmdObj.getIconPixmap(),
                                cmdObj.getCommandName(),
                                cmdObj.getFolderPath())

            fileUtils.saveCode(cmdObj.getCommand(), cmdObj.getCommandName(),
                               cmdObj.getFolderPath(), cmdObj.isPython())

            self.saveSmartshelfSettings()

        iconCreationDialog.accepted.connect(lambda: commandObjCreated())

    def getListByTabName(self, tabName):
        tabWidget = self.ui.tabWidget

        for i in range(tabWidget.count()):
            if tabWidget.tabText(i) == tabName:
                return tabWidget.widget(i)

        return None

    def getTabNameList(self, list):
        tabWidget = self.ui.tabWidget
        return tabWidget.tabText(tabWidget.indexOf(list))

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
