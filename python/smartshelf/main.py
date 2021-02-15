scriptFolder = "H:/sandbox/raphaelJ/smartshelf/python/"
"""
name : reloadAll
description : reload all the smartshelf modules
"""


def reloadAll():
    for i in range(2):
        import smartshelf.component.flatbutton
        reload(smartshelf.component.flatbutton)
        import smartshelf.resource
        reload(smartshelf.resource)

        import smartshelf.ui.settingsdialog
        reload(smartshelf.ui.settingsdialog)


"""
name : compileResources
description : compite the resource file using maya binary files
"""


def compileResources():
    import subprocess
    mayaFolder = "C:/Program Files/Autodesk/Maya2019/bin/"
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


def test():
    import maya.OpenMayaUI as omui
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance

    widget = omui.MQtUtil.findControl("Shelf")
    qwidget = wrapInstance(long(widget), QWidget)

    label = QLabel(qwidget)
    label.setText("Hello!")

    # add label to status line layout
    #qwidget.layout().addWidget(label)

    el = qwidget

    el = el.layout().itemAt(0).widget()
    el = el.layout().itemAt(0).widget()
    el = el.layout().itemAt(1).widget()  # 18 onglets
    nbTabs = el.layout().count()

    customTab = None

    for tabIndex in range(nbTabs):
        curTab = el.layout().itemAt(tabIndex).widget()

        if curTab.objectName() == "Custom":
            customTab = curTab

    print(customTab.layout().count())


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
