from PySide2.QtGui import QPixmap


class CommandObject:
    def __init__(self):
        self.folderPath = None
        self.iconPixmap = None
        self.commandName = None
        self.visibleName = False
        self.command = None
        self.isPythonCode = True
        self.containingTab = None
        self.isLockedCode = False

    def readData(self, cmdObj):
        self.setContainingTab(cmdObj.getContainingTab())
        self.setFolderPath(cmdObj.getFolderPath())
        self.setIconPixmap(QPixmap(cmdObj.getIconPixmap()))
        self.setCommandName(str(cmdObj.getCommandName()))
        self.setIsVisibleName(cmdObj.isVisibleName())
        self.setCommand(cmdObj.getCommand(), cmdObj.isPython())
        self.setIsLocked(cmdObj.isLocked())

    def setContainingTab(self, tabName):
        self.containingTab = tabName

    def getContainingTab(self):
        return self.containingTab

    def setFolderPath(self, path):
        self.folderPath = path

    def getFolderPath(self):
        return self.folderPath.replace("\\", "/")

    def setIconPixmap(self, pixmap):
        self.iconPixmap = pixmap

    def getIconPixmap(self):
        return self.iconPixmap

    def setCommandName(self, name):
        self.commandName = name

    def getCommandName(self):
        return self.commandName

    def setIsVisibleName(self, state):
        self.visibleName = state

    def isVisibleName(self):
        return self.visibleName

    def setCommand(self, command, isPythonCode=True):
        self.command = command
        self.isPythonCode = isPythonCode

    def getCommand(self):
        return self.command

    def isPython(self):
        return self.isPythonCode

    def setIsLocked(self, state):
        self.isLockedCode = state

    def isLocked(self):
        return self.isLockedCode