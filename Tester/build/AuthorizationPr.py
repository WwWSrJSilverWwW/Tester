from PyQt5.QtWidgets import *
from PyQt5 import uic
from build.MakingTestPr import MakingTest
from build.OptionsSy import *


class Authorization(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('build\Designers\AuthorizationDes.ui', self)
        self.setFixedSize(self.size())
        self.setWindowTitle(RU_LABELS["authorization"])
        self.password.setEchoMode(QLineEdit.Password)
        self.okCancel.accepted.connect(self.accepted_def)
        self.okCancel.rejected.connect(self.close)

    def accepted_def(self):
        if self.login.text() == login and self.password.text() == password:
            self.incorrect.clear()
            self.mkt = MakingTest()
            self.mkt.show()
            self.close()
        else:
            QMessageBox.about(self, RU_LABELS["warning"], RU_LABELS["badLoginPassword"])
            self.password.clear()
