# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/Documents/maya/2020/prefs/scripts/smartshelf/python/smartshelf/ui/iconsearchdialog.ui'
#
# Created: Fri Feb 26 17:09:59 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_iconSearchDialog(object):
    def setupUi(self, iconSearchDialog):
        iconSearchDialog.setObjectName("iconSearchDialog")
        iconSearchDialog.resize(529, 348)
        self.verticalLayout = QtWidgets.QVBoxLayout(iconSearchDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.iconsWidget = QtWidgets.QWidget(iconSearchDialog)
        self.iconsWidget.setObjectName("iconsWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.iconsWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.searchEdit = QtWidgets.QLineEdit(self.iconsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchEdit.sizePolicy().hasHeightForWidth())
        self.searchEdit.setSizePolicy(sizePolicy)
        self.searchEdit.setMinimumSize(QtCore.QSize(120, 0))
        self.searchEdit.setObjectName("searchEdit")
        self.horizontalLayout.addWidget(self.searchEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.listWidget = IconListWidget(self.iconsWidget)
        self.listWidget.setStyleSheet("QListWidget::item:selected {\n"
"     background-color: #5285a6;\n"
"}\n"
"")
        self.listWidget.setMovement(QtWidgets.QListView.Static)
        self.listWidget.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget.setProperty("isWrapping", True)
        self.listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget.setSpacing(3)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.horizontalLayout_2.addWidget(self.iconsWidget)
        self.loadingWidget = QtWidgets.QWidget(iconSearchDialog)
        self.loadingWidget.setObjectName("loadingWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.loadingWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.progressBar = QtWidgets.QProgressBar(self.loadingWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_4.addWidget(self.progressBar)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_2.addWidget(self.loadingWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(iconSearchDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(iconSearchDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), iconSearchDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), iconSearchDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(iconSearchDialog)

    def retranslateUi(self, iconSearchDialog):
        iconSearchDialog.setWindowTitle(QtWidgets.QApplication.translate("iconSearchDialog", "Default icon browser", None, -1))
        self.searchEdit.setPlaceholderText(QtWidgets.QApplication.translate("iconSearchDialog", "Search an icon ...", None, -1))

from smartshelf.component.iconlistwidget import IconListWidget
