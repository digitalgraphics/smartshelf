# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/Documents/maya/2020/prefs/scripts/smartshelf/python/smartshelf/ui/iconwidget.ui'
#
# Created: Sat Feb 20 12:25:52 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_iconWidget(object):
    def setupUi(self, iconWidget):
        iconWidget.setObjectName("iconWidget")
        iconWidget.resize(149, 97)
        iconWidget.setStyleSheet("QWidget:hover{\n"
"    background: rgba(255, 255, 255, 10%)\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(iconWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(iconWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(iconWidget)
        QtCore.QMetaObject.connectSlotsByName(iconWidget)

    def retranslateUi(self, iconWidget):
        iconWidget.setWindowTitle(QtWidgets.QApplication.translate("iconWidget", "Form", None, -1))

