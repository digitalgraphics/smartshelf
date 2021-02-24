from smartshelf.ui.smartshelfwidget import Ui_SmartshelfWidget
from PySide2.QtWidgets import QWidget


class SmartshelfWidget(QWidget):
    def __init__(self, parent=None):
        super(SmartshelfWidget, self).__init__(parent)
        self.ui = Ui_SmartshelfWidget()
        self.ui.setupUi(self)
