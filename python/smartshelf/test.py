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
