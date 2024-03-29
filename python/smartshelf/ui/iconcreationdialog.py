# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/Documents/maya/2020/prefs/scripts/smartshelf/python/smartshelf/ui/iconcreationdialog.ui'
#
# Created: Fri Feb 26 17:09:59 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_iconCreationDialog(object):
    def setupUi(self, iconCreationDialog):
        iconCreationDialog.setObjectName("iconCreationDialog")
        iconCreationDialog.resize(527, 571)
        self.verticalLayout = QtWidgets.QVBoxLayout(iconCreationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(iconCreationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.iconPreviewLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconPreviewLabel.sizePolicy().hasHeightForWidth())
        self.iconPreviewLabel.setSizePolicy(sizePolicy)
        self.iconPreviewLabel.setObjectName("iconPreviewLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.iconPreviewLabel)
        self.iconPreviewWidget = QtWidgets.QWidget(self.groupBox)
        self.iconPreviewWidget.setObjectName("iconPreviewWidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.iconPreviewWidget)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.iconThumbnail = IconThumbnail(self.iconPreviewWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconThumbnail.sizePolicy().hasHeightForWidth())
        self.iconThumbnail.setSizePolicy(sizePolicy)
        self.iconThumbnail.setMinimumSize(QtCore.QSize(64, 64))
        self.iconThumbnail.setMaximumSize(QtCore.QSize(64, 64))
        self.iconThumbnail.setObjectName("iconThumbnail")
        self.horizontalLayout_3.addWidget(self.iconThumbnail)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.browseFolderButton = FlatButton(self.iconPreviewWidget)
        self.browseFolderButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/changeDirectory.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browseFolderButton.setIcon(icon)
        self.browseFolderButton.setIconSize(QtCore.QSize(14, 16))
        self.browseFolderButton.setObjectName("browseFolderButton")
        self.verticalLayout_5.addWidget(self.browseFolderButton)
        spacerItem = QtWidgets.QSpacerItem(20, 4, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem)
        self.browseFavouriteButton = FlatButton(self.iconPreviewWidget)
        self.browseFavouriteButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/favoriteStar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browseFavouriteButton.setIcon(icon1)
        self.browseFavouriteButton.setIconSize(QtCore.QSize(14, 16))
        self.browseFavouriteButton.setObjectName("browseFavouriteButton")
        self.verticalLayout_5.addWidget(self.browseFavouriteButton)
        self.widget = QtWidgets.QWidget(self.iconPreviewWidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_5.addWidget(self.widget)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.iconPreviewWidget)
        self.shortcutNameLabel_2 = QtWidgets.QLabel(self.groupBox)
        self.shortcutNameLabel_2.setObjectName("shortcutNameLabel_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.shortcutNameLabel_2)
        self.shortcutNameWidget = QtWidgets.QWidget(self.groupBox)
        self.shortcutNameWidget.setObjectName("shortcutNameWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.shortcutNameWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.nameEdit = QtWidgets.QLineEdit(self.shortcutNameWidget)
        self.nameEdit.setObjectName("nameEdit")
        self.horizontalLayout_2.addWidget(self.nameEdit)
        self.visibleCheckBox = QtWidgets.QCheckBox(self.shortcutNameWidget)
        self.visibleCheckBox.setObjectName("visibleCheckBox")
        self.horizontalLayout_2.addWidget(self.visibleCheckBox)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.shortcutNameWidget)
        self.containingTabLabel_2 = QtWidgets.QLabel(self.groupBox)
        self.containingTabLabel_2.setObjectName("containingTabLabel_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.containingTabLabel_2)
        self.containingTabWidget = QtWidgets.QWidget(self.groupBox)
        self.containingTabWidget.setObjectName("containingTabWidget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.containingTabWidget)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.containingTabComboBox = QtWidgets.QComboBox(self.containingTabWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.containingTabComboBox.sizePolicy().hasHeightForWidth())
        self.containingTabComboBox.setSizePolicy(sizePolicy)
        self.containingTabComboBox.setObjectName("containingTabComboBox")
        self.horizontalLayout_7.addWidget(self.containingTabComboBox)
        self.addTabButton = FlatButton(self.containingTabWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addTabButton.sizePolicy().hasHeightForWidth())
        self.addTabButton.setSizePolicy(sizePolicy)
        self.addTabButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addTabButton.setIcon(icon2)
        self.addTabButton.setObjectName("addTabButton")
        self.horizontalLayout_7.addWidget(self.addTabButton)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_7)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.containingTabWidget)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(iconCreationDialog)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.pythonButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.pythonButton.setChecked(True)
        self.pythonButton.setObjectName("pythonButton")
        self.horizontalLayout_4.addWidget(self.pythonButton)
        self.melButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.melButton.setObjectName("melButton")
        self.horizontalLayout_4.addWidget(self.melButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.codeTextEdit = CodePlainTextEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(9)
        self.codeTextEdit.setFont(font)
        self.codeTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.codeTextEdit.setPlainText("")
        self.codeTextEdit.setTabStopWidth(30)
        self.codeTextEdit.setObjectName("codeTextEdit")
        self.verticalLayout_4.addWidget(self.codeTextEdit)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.runButton = QtWidgets.QPushButton(iconCreationDialog)
        self.runButton.setObjectName("runButton")
        self.horizontalLayout_5.addWidget(self.runButton)
        self.okButton = QtWidgets.QPushButton(iconCreationDialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_5.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(iconCreationDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_5.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(iconCreationDialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("clicked()"), iconCreationDialog.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), iconCreationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(iconCreationDialog)

    def retranslateUi(self, iconCreationDialog):
        iconCreationDialog.setWindowTitle(QtWidgets.QApplication.translate("iconCreationDialog", "Command creation", None, -1))
        self.iconPreviewLabel.setText(QtWidgets.QApplication.translate("iconCreationDialog", "Icon Preview", None, -1))
        self.shortcutNameLabel_2.setText(QtWidgets.QApplication.translate("iconCreationDialog", "Command Name", None, -1))
        self.visibleCheckBox.setText(QtWidgets.QApplication.translate("iconCreationDialog", "visible", None, -1))
        self.containingTabLabel_2.setText(QtWidgets.QApplication.translate("iconCreationDialog", "Containing Tab", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("iconCreationDialog", "Command", None, -1))
        self.pythonButton.setText(QtWidgets.QApplication.translate("iconCreationDialog", "Python", None, -1))
        self.melButton.setText(QtWidgets.QApplication.translate("iconCreationDialog", "MEL", None, -1))
        self.runButton.setText(QtWidgets.QApplication.translate("iconCreationDialog", "Run", None, -1))
        self.okButton.setText(QtWidgets.QApplication.translate("iconCreationDialog", "OK", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("iconCreationDialog", "Cancel", None, -1))

from smartshelf.component.codeplaintextedit import CodePlainTextEdit
from smartshelf.component.iconthumbnail import IconThumbnail
from smartshelf.component.flatbutton import FlatButton
from smartshelf.resource import resource_rc
