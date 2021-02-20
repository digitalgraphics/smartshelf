class CommandObject:
    def __init__(self):
        self.iconPath = None
        self.commandName = None
        self.visibleName = False
        self.command = None
        self.isPython = True

    def setIconPath(self, path):
        self.iconPath = path

    def getIconPath(self):
        return self.iconPath

    def setCommandName(self, name):
        self.commandName = name

    def getCommandName(self):
        return self.commandName

    def setVisibleName(self, state):
        self.visibleName = state

    def isVisibleName(self):
        return self.visibleName

    def setCommand(self, command, isPython=True):
        self.command = command
        self.isPython = isPython