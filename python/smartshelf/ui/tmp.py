# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/Documents/maya/2020/prefs/scripts/smartshelf/python/smartshelf/ui/smartshelfwidget.ui'
#
# Created: Wed Feb 24 18:41:23 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SmartshelfWidget(object):
    def setupUi(self, SmartshelfWidget):
        SmartshelfWidget.setObjectName("SmartshelfWidget")
        SmartshelfWidget.resize(538, 136)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SmartshelfWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(SmartshelfWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(SmartshelfWidget)
        QtCore.QMetaObject.connectSlotsByName(SmartshelfWidget)

    def retranslateUi(self, SmartshelfWidget):
        SmartshelfWidget.setWindowTitle(QtWidgets.QApplication.translate("SmartshelfWidget", "Form", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("SmartshelfWidget", "PushButton", None, -1))

