# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/Documents/maya/2020/prefs/scripts/smartshelf/python/smartshelf/ui/settingsdialog.ui'
#
# Created: Thu Feb 25 14:54:51 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_settingsDialog(object):
    def setupUi(self, settingsDialog):
        settingsDialog.setObjectName("settingsDialog")
        settingsDialog.resize(465, 476)
        self.verticalLayout = QtWidgets.QVBoxLayout(settingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(settingsDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tabsWidget = QtWidgets.QWidget(self.groupBox)
        self.tabsWidget.setObjectName("tabsWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tabsWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QListWidget(self.tabsWidget)
        self.tabWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.addTabButton = QtWidgets.QPushButton(self.tabsWidget)
        self.addTabButton.setObjectName("addTabButton")
        self.verticalLayout_4.addWidget(self.addTabButton)
        self.editTabButton = QtWidgets.QPushButton(self.tabsWidget)
        self.editTabButton.setObjectName("editTabButton")
        self.verticalLayout_4.addWidget(self.editTabButton)
        self.removeTabButton = QtWidgets.QPushButton(self.tabsWidget)
        self.removeTabButton.setObjectName("removeTabButton")
        self.verticalLayout_4.addWidget(self.removeTabButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_7.addWidget(self.tabsWidget)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(settingsDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.visibleIconsWidget = QtWidgets.QWidget(self.groupBox_3)
        self.visibleIconsWidget.setObjectName("visibleIconsWidget")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.visibleIconsWidget)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.sharedCmdButton = QtWidgets.QRadioButton(self.visibleIconsWidget)
        self.sharedCmdButton.setObjectName("sharedCmdButton")
        self.verticalLayout_9.addWidget(self.sharedCmdButton)
        self.privateCmdButton = QtWidgets.QRadioButton(self.visibleIconsWidget)
        self.privateCmdButton.setObjectName("privateCmdButton")
        self.verticalLayout_9.addWidget(self.privateCmdButton)
        self.allCmdButton = QtWidgets.QRadioButton(self.visibleIconsWidget)
        self.allCmdButton.setChecked(True)
        self.allCmdButton.setObjectName("allCmdButton")
        self.verticalLayout_9.addWidget(self.allCmdButton)
        self.verticalLayout_8.addWidget(self.visibleIconsWidget)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(settingsDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.iconSizeWidget = QtWidgets.QWidget(self.groupBox_2)
        self.iconSizeWidget.setObjectName("iconSizeWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.iconSizeWidget)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.size32Button = QtWidgets.QRadioButton(self.iconSizeWidget)
        self.size32Button.setChecked(True)
        self.size32Button.setObjectName("size32Button")
        self.verticalLayout_5.addWidget(self.size32Button)
        self.size64Button = QtWidgets.QRadioButton(self.iconSizeWidget)
        self.size64Button.setObjectName("size64Button")
        self.verticalLayout_5.addWidget(self.size64Button)
        self.verticalLayout_6.addWidget(self.iconSizeWidget)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_4 = QtWidgets.QGroupBox(settingsDialog)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.clearOrganisationButton = QtWidgets.QPushButton(self.groupBox_4)
        self.clearOrganisationButton.setObjectName("clearOrganisationButton")
        self.horizontalLayout_5.addWidget(self.clearOrganisationButton)
        self.clearAllButton = QtWidgets.QPushButton(self.groupBox_4)
        self.clearAllButton.setObjectName("clearAllButton")
        self.horizontalLayout_5.addWidget(self.clearAllButton)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(settingsDialog)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.settingsPathEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.settingsPathEdit.setEnabled(False)
        self.settingsPathEdit.setReadOnly(True)
        self.settingsPathEdit.setObjectName("settingsPathEdit")
        self.horizontalLayout.addWidget(self.settingsPathEdit)
        self.verticalLayout_3.addWidget(self.groupBox_5)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.infoButton = FlatButton(settingsDialog)
        self.infoButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.infoButton.setIcon(icon)
        self.infoButton.setObjectName("infoButton")
        self.horizontalLayout_3.addWidget(self.infoButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.okButton = QtWidgets.QPushButton(settingsDialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_3.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(settingsDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_3.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(settingsDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), settingsDialog.reject)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("clicked()"), settingsDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(settingsDialog)

    def retranslateUi(self, settingsDialog):
        settingsDialog.setWindowTitle(QtWidgets.QApplication.translate("settingsDialog", "Dialog", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("settingsDialog", "Tabs", None, -1))
        self.addTabButton.setText(QtWidgets.QApplication.translate("settingsDialog", "Add", None, -1))
        self.editTabButton.setText(QtWidgets.QApplication.translate("settingsDialog", "Rename", None, -1))
        self.removeTabButton.setText(QtWidgets.QApplication.translate("settingsDialog", "Remove", None, -1))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("settingsDialog", "Visible commands", None, -1))
        self.sharedCmdButton.setText(QtWidgets.QApplication.translate("settingsDialog", "Only shared commands", None, -1))
        self.privateCmdButton.setText(QtWidgets.QApplication.translate("settingsDialog", "Only private commands", None, -1))
        self.allCmdButton.setText(QtWidgets.QApplication.translate("settingsDialog", "Shared and private commands", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("settingsDialog", "Icon size", None, -1))
        self.size32Button.setText(QtWidgets.QApplication.translate("settingsDialog", "32 px", None, -1))
        self.size64Button.setText(QtWidgets.QApplication.translate("settingsDialog", "64 px", None, -1))
        self.groupBox_4.setTitle(QtWidgets.QApplication.translate("settingsDialog", "User settings", None, -1))
        self.clearOrganisationButton.setText(QtWidgets.QApplication.translate("settingsDialog", "Clear organisation", None, -1))
        self.clearAllButton.setText(QtWidgets.QApplication.translate("settingsDialog", "Clear all", None, -1))
        self.groupBox_5.setTitle(QtWidgets.QApplication.translate("settingsDialog", "Settings path", None, -1))
        self.okButton.setText(QtWidgets.QApplication.translate("settingsDialog", "OK", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("settingsDialog", "Cancel", None, -1))

from smartshelf.component.flatbutton import FlatButton
from smartshelf.resource import resource_rc
