from PyQt5.QtWidgets import *
from PyQt5 import uic
from build.MakingTestPr import MakingTest
from build.OptionsSy import *


class Authorization(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('build\Designers\AuthorizationDes.ui', self)
        self.setFixedSize(int(0.2 * fixedSize[0]), int(0.2 * fixedSize[1]))
        x = (QApplication.desktop().width() - self.size().width()) // 2
        y = (QApplication.desktop().height() - self.size().height()) // 2
        self.setGeometry(x, y, self.size().width(), self.size().height())
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
