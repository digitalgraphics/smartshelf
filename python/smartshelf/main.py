scriptFolder = "D:/Documents/maya/2020/prefs/scripts/smartshelf/python/"
# scriptFolder = "H:/sandbox/raphaelJ/smartshelf/python/"
"""
name : reloadAll
description : reload all the smartshelf modules
"""


def reloadAll():
    for i in range(2):

        import smartshelf.component.commandobject
        reload(smartshelf.component.commandobject)
        import smartshelf.component.flatbutton
        reload(smartshelf.component.flatbutton)
        import smartshelf.resource
        reload(smartshelf.resource)

        import smartshelf.utils.dock
        reload(smartshelf.utils.dock)
        import smartshelf.utils.mayautils
        reload(smartshelf.utils.mayautils)
        import smartshelf.utils.file
        reload(smartshelf.utils.file)

        import smartshelf.component.iconwidget
        reload(smartshelf.component.iconwidget)
        import smartshelf.component.iconlistwidget
        reload(smartshelf.component.iconlistwidget)
        import smartshelf.component.pythonhighlighter
        reload(smartshelf.component.pythonhighlighter)
        import smartshelf.component.codeplaintextedit
        reload(smartshelf.component.codeplaintextedit)
        import smartshelf.component.iconthumbnail
        reload(smartshelf.component.iconthumbnail)

        import smartshelf.view.iconsearchdialog
        reload(smartshelf.view.iconsearchdialog)
        import smartshelf.view.iconcreationdialog
        reload(smartshelf.view.iconcreationdialog)
        import smartshelf.view.mainwindow
        reload(smartshelf.view.mainwindow)

        import smartshelf.ui.iconcreationdialog
        reload(smartshelf.ui.iconcreationdialog)
        import smartshelf.ui.iconsearchdialog
        reload(smartshelf.ui.iconsearchdialog)
        import smartshelf.ui.iconwidget
        reload(smartshelf.ui.iconwidget)
        import smartshelf.ui.mainwindow
        reload(smartshelf.ui.mainwindow)


"""
name : compileResources
description : compite the resource file using maya binary files
"""


def compileResources():
    import subprocess
    mayaFolder = "C:/Program Files/Autodesk/Maya2019/bin/"
    # mayaFolder = "C:/Program Files/Autodesk/Maya2018/bin/"
    qrcFilename = 'smartshelf/resource/resource.qrc'
    bashCommand = [
        mayaFolder + "pyside2-rcc.exe", scriptFolder + qrcFilename, "-o",
        scriptFolder + qrcFilename.replace(".qrc", "_rc.py")
    ]

    process = subprocess.Popen(bashCommand,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, err = process.communicate()


"""
name : compileUis
description : compile all the ui files from smartshelf/ui to py files
"""


def compileUis():
    from pyside2uic import compileUi
    import os

    uiPath = scriptFolder + 'smartshelf/ui'
    for file in os.listdir(uiPath):
        if file.endswith(".ui"):
            file = uiPath + "/" + file
            print("compile : " + file)
            tmp = uiPath + '/tmp.py'

            uiOutput = open(tmp, "w")
            compileUi(file, uiOutput, False, 4, False)
            uiOutput.close()

            fin = open(tmp, "rt")
            fout = open(file.replace(".ui", ".py"), "wt")

            for line in fin:
                fout.write(
                    line.replace(
                        'import resource_rc',
                        'from smartshelf.resource import resource_rc'))

            fin.close()
            fout.close()


"""
name : run
param : 
    - needCompileresources : True to recompile the resource file
    - needCompileUis : True to compile all the ui from smartshelf/ui
    - needReloadAll : True to reload all the smartshelf modules
description : run the main smartshelf window
"""


def run(needCompileResources=False, needCompileUis=False, needReloadAll=False):

    if needCompileResources:
        compileResources()

    if needCompileUis:
        compileUis()

    if needReloadAll:
        reloadAll()

    import smartshelf.utils.dock as dockUtils

    from smartshelf.view.mainwindow import MainWindow

    mainWindow = dockUtils.dockify(MainWindow, "Smartshelf")
