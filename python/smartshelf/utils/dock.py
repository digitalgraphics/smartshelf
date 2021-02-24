from maya import cmds
from maya import OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance


def maya_main_window():
    '''
        Return the Maya main window widget as a Python object
        '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def dockify(windowClass, name, show=True):
    """Dock `Widget` into Maya
    Arguments:
        Widget (QWidget): Class
        show (bool, optional): Whether to show the resulting dock once created
    """

    try:
        cmds.deleteUI(name)
    except RuntimeError:
        pass

    dockControl = cmds.workspaceControl(name,
                                        tabToControl=["AttributeEditor", -1],
                                        label=name,
                                        widthProperty='prefered')

    dockPtr = omui.MQtUtil.findControl(dockControl)
    dockWidget = wrapInstance(long(dockPtr), QtWidgets.QWidget)
    dockWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    windowChild = windowClass(maya_main_window())
    dockWidget.layout().addWidget(windowChild)

    if show:
        cmds.evalDeferred(lambda *args: cmds.workspaceControl(
            dockControl, edit=True, restore=True))

    return windowChild
