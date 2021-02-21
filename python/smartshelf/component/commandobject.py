class CommandObject:
    def __init__(self):
        self.folderPath = None
        self.iconPixmap = None
        self.commandName = None
        self.visibleName = False
        self.command = None
        self.isPythonCode = True

    def setFolderPath(self, path):
        self.folderPath = path

    def getFolderPath(self):
        return self.folderPath

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